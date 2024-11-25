from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, mock_open
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

    @patch("transaction.views.db")
    @patch("transaction.views.os.getenv")
    @patch("transaction.views.open", new_callable=mock_open)
    def test_upload_data_to_firestore_success(self, mock_file, mock_getenv, mock_db):
        """
        Test successful upload of data to Firestore
        """
        # Mock getenv to return a path
        mock_getenv.return_value = "/mock/path/to/data.json"

        # Mock file opening and json loading
        mock_file.return_value.read.return_value = json.dumps(self.mock_json_data)

        # Mock Firestore methods
        mock_db.collection.return_value.document.return_value.set.return_value = None
        mock_db.collection.return_value.limit.return_value.get.return_value = []

        # Create a mock request
        from django.test import RequestFactory

        request = RequestFactory().post("/transaction/upload")

        # Call the function
        response = upload_data_to_firestore(request)

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", json.loads(response.content))

    @patch("transaction.views.db")
    def test_get_data_from_firestore_success(self, mock_db):
        """
        Test successful retrieval of data from Firestore
        """
        # Create mock documents
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

        # Create a mock request
        from django.test import RequestFactory

        request = RequestFactory().get("/transaction/get")

        # Call the function
        response = get_data_from_firestore(request)

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)

        # Parse the response content
        transactions = json.loads(response.content)
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0]["Company Name"], "TestCompany")

    @patch("transaction.views.db")
    def test_get_data_from_firestore_exception(self, mock_db):
        """
        Test error handling in get_data_from_firestore
        """
        # Simulate an exception when streaming data
        mock_db.collection.return_value.stream.side_effect = Exception("Database error")

        # Create a mock request
        from django.test import RequestFactory

        request = RequestFactory().get("/transaction/get")

        # Call the function
        response = get_data_from_firestore(request)

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 500)
        error_data = json.loads(response.content)
        self.assertIn("error", error_data)
