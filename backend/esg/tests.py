from django.test import TestCase, RequestFactory
from unittest.mock import patch, mock_open, MagicMock
from django.http import JsonResponse
import json
from esg.views import ESGView

class ESGViewTests(TestCase):
    """
    Test cases for ESGView class.
    """

    def setUp(self):
        self.view = ESGView()
        self.factory = RequestFactory()
        self.mock_esg_data = [
            {"name": "CompanyA", "environment_score": 300, "social_score": 305, "governance_score": 310},
            {"name": "CompanyB", "environment_score": 450, "social_score": 200, "governance_score": 500},
        ]


    @patch("esg.views.db")
    def test_get_data_from_firestore_success(self, mock_db):
        """
        Test successful retrieval of all ESG data from Firestore.
        """
        # Mock Firestore documents
        mock_docs = [
            MagicMock(to_dict=lambda: {"name": "Subway", "environment_score": 200}),
            MagicMock(to_dict=lambda: {"name": "Walmart", "environment_score": 300}),
        ]
        mock_db.collection.return_value.stream.return_value = mock_docs

        # Create a mock GET request
        request = self.factory.get("/esg/get")

        # Call the view
        response = self.view.get_data_from_firestore(request)

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)

        expected_data = [
            {"name": "Subway", "environment_score": 200},
            {"name": "Walmart", "environment_score": 300},
        ]
        self.assertJSONEqual(response.content.decode("utf-8"), expected_data)
