import json
import os
from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.http import JsonResponse
from django.conf import settings

from views import upload_data_to_firestore, get_data_from_firestore, get_individual_company_score

class FirestoreViewsTestCase(TestCase):
    def setUp(self):
        # Sample ESG data for testing
        self.sample_esg_data = [
            {
                "name": "TechCorp",
                "merchant_name": "TechCorp Inc",
                "environmental_score": 85,
                "social_score": 90,
                "governance_score": 88
            },
            {
                "name": "GreenEnergy",
                "merchant_name": "GreenEnergy LLC",
                "environmental_score": 95,
                "social_score": 92,
                "governance_score": 94
            }
        ]

    @patch('views.load_dotenv')
    @patch('views.os.getenv')
    @patch('views.open', create=True)
    @patch('views.db')
    @patch('views.json.load')
    def test_upload_data_to_firestore_success(self, mock_json_load, mock_db, mock_open, mock_getenv, mock_load_dotenv):
        # Setup mock objects
        mock_load_dotenv.return_value = None
        mock_getenv.return_value = '/fake/path/esg_data.json'
        mock_open.return_value.__enter__.return_value = MagicMock()
        mock_json_load.return_value = self.sample_esg_data
        
        # Mock Firestore collection and document methods
        mock_collection = MagicMock()
        mock_db.collection.return_value = mock_collection
        mock_collection.get.return_value = [MagicMock()]  # Simulating existing collection
        
        # Create a mock request
        mock_request = MagicMock()

        # Call the function
        response = upload_data_to_firestore(mock_request)

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'message': 'Esg data uploaded successfully'})

        # Verify Firestore interactions
        mock_db.collection.assert_any_call('test')
        mock_db.collection.assert_any_call('esg')
        
        # Check if documents were set correctly
        calls = mock_collection.document.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertIn('TechCorp', [call[0][0] for call in calls])
        self.assertIn('GreenEnergy', [call[0][0] for call in calls])

    @patch('views.db')
    def test_get_data_from_firestore_success(self, mock_db):
        # Create mock documents
        mock_docs = [
            MagicMock(to_dict=lambda: self.sample_esg_data[0]),
            MagicMock(to_dict=lambda: self.sample_esg_data[1])
        ]
        
        # Setup stream to return mock documents
        mock_db.collection.return_value.stream.return_value = mock_docs
        
        # Create a mock request
        mock_request = MagicMock()

        # Call the function
        response = get_data_from_firestore(mock_request)

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        
        # Parse the response content
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]['name'], 'TechCorp')
        self.assertEqual(response_data[1]['name'], 'GreenEnergy')

    @patch('views.db')
    def test_get_individual_company_score_success(self, mock_db):
        # Create a mock document
        mock_doc = MagicMock(to_dict=lambda: self.sample_esg_data[0])
        
        # Setup where clause and stream
        mock_collection = MagicMock()
        mock_db.collection.return_value = mock_collection
        mock_collection.where.return_value.limit.return_value.stream.return_value = [mock_doc]

        # Call the function
        response = get_individual_company_score('TechCorp Inc')

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)

    @patch('views.db')
    def test_upload_data_to_firestore_exception(self, mock_db):
        # Simulate an exception during upload
        mock_db.collection.side_effect = Exception('Firestore connection error')
        
        # Create a mock request
        mock_request = MagicMock()

        # Call the function
        response = upload_data_to_firestore(mock_request)

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 500)
        error_response = json.loads(response.content)
        self.assertIn('error', error_response)

    @patch('views.db')
    def test_get_data_from_firestore_exception(self, mock_db):
        # Simulate an exception during data retrieval
        mock_db.collection.side_effect = Exception('Firestore retrieval error')
        
        # Create a mock request
        mock_request = MagicMock()

        # Call the function
        response = get_data_from_firestore(mock_request)

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 500)
        error_response = json.loads(response.content)
        self.assertIn('error', error_response)

    @patch('views.db')
    def test_get_individual_company_score_exception(self, mock_db):
        # Simulate an exception during individual company score retrieval
        mock_db.collection.side_effect = Exception('Firestore company retrieval error')

        # Call the function
        response = get_individual_company_score('TechCorp Inc')

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 500)
        error_response = json.loads(response.content)
        self.assertIn('error', error_response)