from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, mock_open
from django.http import JsonResponse
import json

from transaction.views import (
    upload_data_to_firestore, 
    get_data_from_firestore, 
    esg_rating
)
from transaction.models import Transaction

# To test locally: heroku local:run python manage.py test
class ViewsTestCase(TestCase):
    def setUp(self):
        # Sample mock data for testing
        self.mock_json_data = {
            'data': [
                {
                    'transactionID': '1',
                    'ip_address': '143.15.148.251',
                    'Company Name': 'TestCompany',
                    'amount': 100.50
                },
                {
                    'transactionID': '2',
                    'ip_address': '36.183.96.60',
                    'Company Name': 'AnotherCompany',
                    'amount': 250.75
                }
            ]
        }

    @patch('transaction.views.db')
    @patch('transaction.views.os.getenv')
    @patch('transaction.views.open', new_callable=mock_open)
    def test_upload_data_to_firestore_success(self, mock_file, mock_getenv, mock_db):
        """
        Test successful upload of data to Firestore
        """
        # Mock getenv to return a path
        mock_getenv.return_value = '/mock/path/to/data.json'

        # Mock file opening and json loading
        mock_file.return_value.read.return_value = json.dumps(self.mock_json_data)

        # Mock Firestore methods
        mock_db.collection.return_value.document.return_value.set.return_value = None
        mock_db.collection.return_value.limit.return_value.get.return_value = []

        # Create a mock request
        from django.test import RequestFactory
        request = RequestFactory().post('/transaction/upload')

        # Call the function
        response = upload_data_to_firestore(request)

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', json.loads(response.content))

    @patch('transaction.views.db')
    def test_get_data_from_firestore_success(self, mock_db):
        """
        Test successful retrieval of data from Firestore
        """
        # Create mock documents
        mock_docs = [
            type('MockDoc', (), {'to_dict': lambda self: {'Company Name': 'TestCompany', 'amount': 100.50}})(),
            type('MockDoc', (), {'to_dict': lambda self: {'Company Name': 'AnotherCompany', 'amount': 250.75}})()
        ]
        mock_db.collection.return_value.stream.return_value = mock_docs

        # Create a mock request
        from django.test import RequestFactory
        request = RequestFactory().get('/transaction/get')

        # Call the function
        response = get_data_from_firestore(request)

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        
        # Parse the response content
        transactions = json.loads(response.content)
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0]['Company Name'], 'TestCompany')

    def test_esg_rating(self):
        """
        Test the esg_rating function
        """
        # Test with different company names
        test_cases = [
            {'Company Name': 'ShortCo', 'expected': 2},
            {'Company Name': 'MediumCompany', 'expected': 4},
            {'Company Name': 'VeryLongCompanyNameHere', 'expected': 7}
        ]

        for case in test_cases:
            transaction = {'Company Name': case['Company Name']}
            rating = esg_rating(transaction)
            self.assertEqual(rating, case['expected'])

    @patch('transaction.views.db')
    def test_get_data_from_firestore_exception(self, mock_db):
        """
        Test error handling in get_data_from_firestore
        """
        # Simulate an exception when streaming data
        mock_db.collection.return_value.stream.side_effect = Exception('Database error')

        # Create a mock request
        from django.test import RequestFactory
        request = RequestFactory().get('/transaction/get')

        # Call the function
        response = get_data_from_firestore(request)

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 500)
        error_data = json.loads(response.content)
        self.assertIn('error', error_data)

    @patch('transaction.views.db')
    @patch('transaction.views.os.getenv')
    def test_upload_data_to_firestore_exception(self, mock_getenv, mock_db):
        """
        Test error handling in upload_data_to_firestore
        """
        # Simulate an exception during upload
        mock_db.collection.return_value.limit.return_value.get.return_value = []
        mock_db.collection.return_value.document.return_value.set.side_effect = Exception('Upload error')

        # Create a mock request
        from django.test import RequestFactory
        request = RequestFactory().post('/transaction/upload')

        # Call the function
        response = upload_data_to_firestore(request)

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 500)
        error_data = json.loads(response.content)
        self.assertIn('error', error_data)
'''
class TransactionTestCase(TestCase):
    # Mock Firestore database
    @patch('transaction.views.db')
    def test_get_data_success(self, mock_db):
        """
        Test that data is correctly fetched from Firestore and returned as a JSON response.
        """
        # Mock Firestore returning data
        mock_db.collection.return_value.stream.return_value = [
            MockDoc({
                "Transaction ID": "TXN001",
                "Client ID": "CL001",
                "Date": "2024-09-01",
                "Company Name": "EcoMarket",
                "Location - Latitude": "40.7128",
                "Location - Longitude": "-74.006",
                "Transaction Amount": "45.5"
            }),
            MockDoc({
                "Transaction ID": "TXN002",
                "Client ID": "CL002",
                "Date": "2024-09-03",
                "Company Name": "GreenCafe",
                "Location - Latitude": "34.0522",
                "Location - Longitude": "-118.2437",
                "Transaction Amount": "12.75"
            })
        ]

        response = self.client.get(reverse('get_data'))

        # Expected JSON response with added ESG ratings
        expected_response = [
            {
                "Transaction ID": "TXN001",
                "Client ID": "CL001",
                "Date": "2024-09-01",
                "Company Name": "EcoMarket",
                "Location - Latitude": "40.7128",
                "Location - Longitude": "-74.006",
                "Transaction Amount": "45.5",
                "rating": 3  # Rating is len("EcoMarket") // 3
            },
            {
                "Transaction ID": "TXN002",
                "Client ID": "CL002",
                "Date": "2024-09-03",
                "Company Name": "GreenCafe",
                "Location - Latitude": "34.0522",
                "Location - Longitude": "-118.2437",
                "Transaction Amount": "12.75",
                "rating": 3
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)

    def test_esg_rating(self):
        """
        Test that the esg_rating() function is applied to each transaction.
        """
        transaction = {"Company Name": "EcoMarket"}
        rating = esg_rating(transaction)

        # Check if the ESG rating is calculated correctly
        self.assertEqual(rating, 3)  # Rating is len("EcoMarket") // 3

    def test_models_correctness(self):
        """
        Test that the Transaction model is correctly defined.
        """

        transaction = Transaction(
            transaction_id="TXN001",
            client_id="CL001",
            date="2024-09-01",
            company_name="EcoMarket",
            location_latitude=40.7128,
            location_longitude=-74.006,
            transaction_amount=45.5
        )

        # Check if the model is correctly defined
        self.assertEqual(str(transaction), "TXN001 - EcoMarket: $45.5")

# Helper class to mock Firestore document
class MockDoc:
    def __init__(self, data):
        self.data = data

    def to_dict(self):
        return self.data
''' 