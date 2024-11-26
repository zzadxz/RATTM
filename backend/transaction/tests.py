from django.test import TestCase, RequestFactory
from unittest.mock import patch, mock_open, MagicMock
from django.http import JsonResponse
import json

from transaction.views import TransactionView
from transaction.use_case import TransactionUseCase
from transaction.abstract_use_case import AbstractTransactionUseCase


# To test locally: heroku local:run python manage.py test
class ViewsTestCase(TestCase):
    def setUp(self):
        # Sample mock data for testing
        self.mock_json_data = {
            "data": [
                {
                    "transactionID": "1",
                    "ip_address": "143.15.148.251",
                    "Company Name": "TestCompany",
                    "amount": 100.50,
                },
                {
                    "transactionID": "2",
                    "ip_address": "36.183.96.60",
                    "Company Name": "AnotherCompany",
                    "amount": 250.75,
                },
            ]
        }

        # Use a mock for the use case implementation
        self.mock_use_case = MagicMock(spec=AbstractTransactionUseCase)
        self.view = TransactionView(self.mock_use_case)
        self.factory = RequestFactory()

    @patch("transaction.use_case.db")
    @patch("transaction.use_case.os.getenv")
    @patch("transaction.use_case.open", new_callable=mock_open)
    def test_upload_data_to_firestore_success(self, mock_file, mock_getenv, mock_db):
        """
        Test successful upload of data to Firestore
        """
        # Mock environment variable and file reading
        mock_getenv.return_value = "/mock/path/to/data.json"
        mock_file.return_value.read.return_value = json.dumps(self.mock_json_data)

        # Mock Firestore behaviors
        mock_db.collection.return_value.limit.return_value.get.return_value = []

        # Mock use case behavior
        self.mock_use_case.upload_data_to_firestore_use_case.return_value = 1

        # Create a mock POST request
        request = self.factory.post("/transaction/upload")

        # Call the view
        response = self.view.upload_data_to_firestore(request)

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", json.loads(response.content))
        self.mock_use_case.upload_data_to_firestore_use_case.assert_called_once()

    @patch("transaction.use_case.db")
    def test_get_data_from_firestore_success(self, mock_db):
        """
        Test successful retrieval of data from Firestore
        """
        # Mock Firestore documents
        mock_docs = [
            type(
                "MockDoc",
                (),
                {
                    "to_dict": lambda self: {
                        "Company Name": "TestCompany",
                        "amount": 100.50,
                    }
                },
            )(),
            type(
                "MockDoc",
                (),
                {
                    "to_dict": lambda self: {
                        "Company Name": "AnotherCompany",
                        "amount": 250.75,
                    }
                },
            )(),
        ]
        mock_db.collection.return_value.stream.return_value = mock_docs

        # Mock use case behavior
        self.mock_use_case.get_data_from_firestore_use_case.return_value = [
            {"Company Name": "TestCompany", "amount": 100.50},
            {"Company Name": "AnotherCompany", "amount": 250.75},
        ]

        # Create a mock GET request
        request = self.factory.get("/transaction/get")

        # Call the view
        response = self.view.get_data_from_firestore(request)

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)

        # Parse the response content
        transactions = json.loads(response.content)
        self.assertIn("transactions", transactions)
        self.assertEqual(len(transactions["transactions"]), 2)
        self.assertEqual(transactions["transactions"][0]["Company Name"], "TestCompany")

        self.mock_use_case.get_data_from_firestore_use_case.assert_called_once()

    def test_get_data_from_firestore_exception(self):
        """
        Test error handling in get_data_from_firestore
        """
        # Mock use case to simulate an exception
        self.mock_use_case.get_data_from_firestore_use_case.return_value = (
            "Database error"
        )

        # Create a mock GET request
        request = self.factory.get("/transaction/get")

        # Call the view
        response = self.view.get_data_from_firestore(request)

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 500)

        # Parse the response content
        error_data = json.loads(response.content)
        self.assertIn("error", error_data)
        self.assertEqual(error_data["error"], "Database error")
