from django.test import TestCase
from unittest.mock import patch, mock_open, MagicMock
from django.http import JsonResponse
from transaction.views import upload_data_to_firestore, get_data_from_firestore, esg_rating
import json

class FirestoreTestCase(TestCase):
    @patch('transaction.views.os.getenv')  # Mock os.getenv to return the path
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "TXN001": {
            "Transaction ID": "TXN001",
            "Client ID": "CL001",
            "Date": "2024-09-01",
            "Company Name": "EcoMarket",
            "Location - Latitude": "40.7128",
            "Location - Longitude": "-74.006",
            "Transaction Amount": "45.5"
        }
    }))  # Mock open to simulate reading the JSON file
    @patch('transaction.views.db.collection')  # Mock Firestore's db.collection
    def test_upload_data_to_firestore(self, mock_collection, mock_open_file, mock_getenv):
        # Set the environment variable to the mock file path
        mock_getenv.return_value = 'backend/resources/mockdata.json'
        
        # Mock the add method of Firestore collection
        mock_collection.return_value.add = MagicMock()
        
        # Create a fake request object (since this is a Django view)
        request = MagicMock()

        # Call the function you're testing
        response = upload_data_to_firestore(request)

        # Check that the file was opened correctly
        mock_open_file.assert_called_once_with('backend/resources/mockdata.json', 'r')

        # Ensure that data is uploaded to Firestore using add
        mock_collection.return_value.add.assert_called_once_with({
            "Transaction ID": "TXN001",
            "Client ID": "CL001",
            "Date": "2024-09-01",
            "Company Name": "EcoMarket",
            "Location - Latitude": "40.7128",
            "Location - Longitude": "-74.006",
            "Transaction Amount": "45.5"
        })

        # Assert that the response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'Data uploaded successfully'})

    @patch('transaction.views.db.collection')  # Mock Firestore's db.collection
    @patch('transaction.views.esg_rating')  # Mock the esg_rating function
    def test_get_data_from_firestore(self, mock_esg_rating, mock_collection):
        # Mock Firestore's stream method to return fake documents
        mock_docs = [
            MagicMock(id='txn1', to_dict=MagicMock(return_value={'Company Name': 'Company A'})),
            MagicMock(id='txn2', to_dict=MagicMock(return_value={'Company Name': 'Company B'})),
        ]
        mock_collection.return_value.stream.return_value = mock_docs

        # Mock the esg_rating function to return a fixed value
        mock_esg_rating.side_effect = [5, 6]

        # Call the view function
        request = MagicMock()  # Create a fake request object
        response = get_data_from_firestore(request)

        # Assert the response
        expected_data = [
            {"Company Name": "Company A", "rating": 5},
            {"Company Name": "Company B", "rating": 6}
        ]
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_data)

    # Not implemented
    def test_esg_rating(self):
        transaction_dict = {"Company Name": 123}
        rating = esg_rating(transaction_dict)
        self.assertEqual(rating, 12455) 
