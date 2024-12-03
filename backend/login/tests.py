from django.test import TestCase, RequestFactory
from unittest.mock import patch, mock_open, MagicMock
from django.http import JsonResponse
import json

from transaction.views import TransactionView
from transaction.use_case import TransactionUseCase
from transaction.calculations import Calculations
from transaction.abstract_use_case import AbstractTransactionUseCase
from django.contrib.sessions.middleware import SessionMiddleware


class TransactionViewTests(TestCase):
    def setUp(self):
        # Mock data
        self.mock_json_data = {
            "data": [
                {
                    "transactionID": "1",
                    "ip_address": "143.15.148.251",
                    "merchant_name": "TestCompany",
                    "amount": 100.50,
                },
                {
                    "transactionID": "2",
                    "ip_address": "36.183.96.60",
                    "merchant_name": "AnotherCompany",
                    "amount": 250.75,
                },
            ]
        }

        # Mock calculations and data access
        self.mock_calculations = MagicMock(spec=Calculations)
        self.mock_data_access = MagicMock()
        self.mock_use_case = TransactionUseCase(self.mock_calculations, self.mock_data_access)
        self.view = TransactionView(self.mock_use_case)
        self.factory = RequestFactory()

    def _setup_request(self, session_data=None):
        """Helper to setup a mock request with session."""
        django_request = self.factory.get("/transaction/get")
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(django_request)
        django_request.session.update(session_data or {})
        django_request.session.save()
        return django_request

    @patch("transaction.use_case.db")
    @patch("transaction.use_case.os.getenv")
    @patch("transaction.use_case.open", new_callable=mock_open)
    def test_upload_data_to_firestore_success(self, mock_file, mock_getenv, mock_db):
        """
        Test successful upload of data to Firestore
        """
        # Mock environment and file behavior
        mock_getenv.return_value = "/mock/path/to/data.json"
        mock_file.return_value.read.return_value = json.dumps(self.mock_json_data)
        mock_db.collection.return_value.limit.return_value.get.return_value = []

        # Mock use case behavior
        self.mock_use_case.upload_data_to_firestore_use_case = MagicMock(return_value=1)

        # Mock request
        request = self.factory.post("/transaction/upload")

        # Call the view
        response = self.view.upload_data_to_firestore(request)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode("utf-8"), {"message": "Data uploaded successfully"})

    def test_get_data_from_firestore_success(self):
        """
        Test successful retrieval of transactions with ESG scores.
        """
        # Mock data for use case
        transactions = [
            {"merchant_name": "TestCompany", "esg_score": 50.5},
            {"merchant_name": "AnotherCompany", "esg_score": "N/A"},
        ]
        self.mock_use_case.get_data_from_firestore_use_case = MagicMock(return_value=transactions)

        # Mock request
        session_data = {"user_id": "1"}
        request = self._setup_request(session_data)

        # Call the view
        response = self.view.get_data_from_firestore(request)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode("utf-8"), transactions)

    def test_get_data_from_firestore_no_session(self):
        """
        Test retrieval of transactions when user_id is missing in the session.
        """
        # Mock data for use case
        transactions = [{"merchant_name": "TestCompany", "esg_score": "N/A"}]
        self.mock_use_case.get_data_from_firestore_use_case = MagicMock(return_value=transactions)

        # Mock request without session
        request = self._setup_request()

        # Call the view
        response = self.view.get_data_from_firestore(request)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode("utf-8"), transactions)

    def test_get_data_from_firestore_error(self):
        """
        Test handling of errors during data retrieval.
        """
        self.mock_use_case.get_data_from_firestore_use_case = MagicMock(return_value="Database error")
        request = self._setup_request({"user_id": "1"})

        response = self.view.get_data_from_firestore(request)

        # Assertions
        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(response.content.decode("utf-8"), {"error": "Database error"})


class CalculationsTests(TestCase):
    def setUp(self):
        self.calculations = Calculations()

    def test_get_closest_match(self):
        """
        Test finding the closest match for a company name.
        """
        choices = {"TestCompany": {}, "AnotherCompany": {}}
        match = self.calculations._get_closest_match("TestCmpny", choices)
        self.assertEqual(match, "TestCompany")

        # Test no match
        match = self.calculations._get_closest_match("UnknownCompany", choices)
        self.assertIsNone(match)

    def test_get_company_env_score(self):
        """
        Test retrieval of environmental score for a transaction.
        """
        ESG_scores = {
            "TestCompany": {"environment_score": 50.5},
            "AnotherCompany": {"environment_score": 80.0},
        }

        transaction = {"merchant_name": "TestCompany"}
        score = self.calculations.get_company_env_score(transaction, ESG_scores)
        self.assertEqual(score, 50.5)

        # Test no match
        transaction = {"merchant_name": "UnknownCompany"}
        score = self.calculations.get_company_env_score(transaction, ESG_scores)
        self.assertEqual(score, 0)


class TransactionUseCaseTests(TestCase):
    def setUp(self):
        self.mock_calculations = MagicMock(spec=Calculations)
        self.mock_data_access = MagicMock()
        self.use_case = TransactionUseCase(self.mock_calculations, self.mock_data_access)

    def test_get_data_from_firestore_use_case(self):
        """
        Test processing of transactions and ESG scores.
        """
        self.mock_data_access.get_table_from_database.side_effect = lambda table: {
            "Users": {"1": {"transactions": [{"merchant_name": "TestCompany"}]}},
            "esg": {"TestCompany": {"environment_score": 50.5}},
        }[table]

        self.mock_calculations.get_company_env_score.return_value = 50.5

        transactions = self.use_case.get_data_from_firestore_use_case("1")

        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]["esg_score"], 50.5)

    def test_get_data_from_firestore_use_case_no_scores(self):
        """
        Test handling transactions with no ESG scores.
        """
        self.mock_data_access.get_table_from_database.side_effect = lambda table: {
            "Users": {"1": {"transactions": [{"merchant_name": "UnknownCompany"}]}},
            "esg": {"TestCompany": {"environment_score": 50.5}},
        }[table]

        self.mock_calculations.get_company_env_score.return_value = 0

        transactions = self.use_case.get_data_from_firestore_use_case("1")

        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]["esg_score"], "N/A")
