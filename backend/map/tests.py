import unittest
from unittest.mock import patch, MagicMock
from django.http import JsonResponse
from .use_cases import get_user_all_locations_and_company
from django.test import TestCase

"""
class TestMapFunctions(unittest.TestCase):
    def setUp(self):
        self.mock_user_transactions = [
            {"latitude": 40.7128, "longitude": -74.0060, "merchant_name": "Company A"},
            {"latitude": 34.0522, "longitude": -118.2437, "merchant_name": "Company B"}
        ]

        self.mock_esg_scores = {
            "Company A": {"environment_score": 600},
            "Company B": {"environment_score": 200}
        }

    def test_get_user_all_locations_and_company(self, mock_company_tier, mock_get_closest_match, mock_get_table_from_firebase, mock_db):
        # Mock the user document retrieval
        mock_user_doc = MagicMock()
        mock_user_doc.get.return_value.to_dict.return_value = {
            "transactions": self.mock_user_transactions
        }
        mock_db.collection.return_value.document.return_value = mock_user_doc
        
        # Mock the get_table_from_firebase function to return mock ESG scores
        mock_get_table_from_firebase.return_value = self.mock_esg_scores

        # Execute the function
        result = get_user_all_locations_and_company('test_user_id')
        
        # Check the returned data structure and values
        expected_result = [
            {
                "location": (40.7128, -74.0060),
                "merchant_name": "Company A",
                "merchant_percentile": 4,
            },
            {
                "location": (34.0522, -118.2437),
                "merchant_name": "Company B",
                "merchant_percentile": 1,
            },
        ]

        # Assert the response matches expected data
        self.assertEqual(result, expected_result)
        
        # Additional assertions to verify function behavior
        mock_db.collection.assert_called_with('Users')
        mock_get_table_from_firebase.assert_called_once_with('esg')

"""

        