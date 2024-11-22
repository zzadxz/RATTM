from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, mock_open
from django.http import JsonResponse
import json

from transaction.views import esg_rating
from transaction.models import Transaction

# To test locally: heroku local:run python manage.py test

class TransactionTestCase(TestCase):
    """
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
        """
    
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
