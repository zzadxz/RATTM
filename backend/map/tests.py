from django.test import TestCase, RequestFactory
from django.urls import reverse
from unittest.mock import patch, MagicMock
from django.http import JsonResponse
import json
from map.views import MapView
from django.contrib.sessions.middleware import SessionMiddleware
from map.views import MapView
from map.abstract_use_case import AbstractMapUseCase
from map.calculations import (
    _get_closest_match, 
    _company_tier, 
)

class ViewsTestCase(TestCase):
    """
    Test MapView and its interaction with MapUseCase.
    """

    def setUp(self):
        # Sample mock data for testing
        self.mock_map_use_case = MagicMock(spec=AbstractMapUseCase)
        self.view = MapView(self.mock_map_use_case)
        self.factory = RequestFactory()

    def _setup_request_with_session(self, method, path, session_data=None):
        """
        Helper function to create a request and attach session data.
        """
        if method.lower() == "get":
            request = self.factory.get(path)
        else:
            raise ValueError("Unsupported method")

        # Attach session middleware
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        if session_data:
            request.session.update(session_data)
        request.session.save()
        return request

    def test_get_map_data_with_session(self):
        """
        Test that MapView.get_map_data works when session contains user_id.
        """
        # Mock session data
        session_data = {"user_id": "123"}

        # Mock use case behavior
        expected_map_data = [
            {
                "location": [88.26035, 75.466192],
                "merchant_name": "Uber",
                "merchant_percentile": 3,
            },
            {
                "location": [17.020551, -57.127564],
                "merchant_name": "McDonalds",
                "merchant_percentile": 3,
            },
        ]
        self.mock_map_use_case.get_user_all_locations_and_company.return_value = (
            expected_map_data
        )

        # Setup request with session
        request = self._setup_request_with_session(
            "get", "/map/get_map_data/", session_data
        )

        # Call the view method
        response = self.view.get_map_data(request)

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)

        actual_map_data = json.loads(response.content)
        self.assertEqual(actual_map_data, expected_map_data)

        # Verify the use case is called with the correct user_id
        self.mock_map_use_case.get_user_all_locations_and_company.assert_called_once_with(
            "123"
        )

    def test_get_map_data_no_session(self):
        """
        Test that MapView.get_map_data defaults to user_id='0' when no session data is available.
        """
        # Mock use case behavior
        expected_map_data = [
            {
                "location": [-51.878229, -79.332151],
                "merchant_name": "Amazon",
                "merchant_percentile": 1,
            },
            {
                "location": [39.796356, 167.669685],
                "merchant_name": "Walmart",
                "merchant_percentile": 4,
            },
        ]
        self.mock_map_use_case.get_user_all_locations_and_company.return_value = (
            expected_map_data
        )

        # Setup request without session data
        request = self._setup_request_with_session("get", "/map/get_map_data/")

        # Call the view method
        response = self.view.get_map_data(request)

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)

        actual_map_data = json.loads(response.content)
        self.assertEqual(actual_map_data, expected_map_data)

        # Verify the use case is called with the default user_id='0'
        self.mock_map_use_case.get_user_all_locations_and_company.assert_called_once_with(
            "0"
        )

    def test_get_map_data_use_case_exception(self):
        """
        Test that MapView.get_map_data handles exceptions raised by the use case.
        """
        # Mock use case to raise an exception
        self.mock_map_use_case.get_user_all_locations_and_company.side_effect = (
            Exception("Unexpected error")
        )

        # Setup request with session
        request = self._setup_request_with_session(
            "get", "/map/get_map_data/", {"user_id": "123"}
        )

        # Call the view method
        with self.assertRaises(Exception) as context:
            self.view.get_map_data(request)

        # Assertions
        self.assertEqual(str(context.exception), "Unexpected error")

        # Verify the use case is called
        self.mock_map_use_case.get_user_all_locations_and_company.assert_called_once_with(
            "123"
        )



class CalculationsTest(TestCase):
    """
    Tests for calculations.py. 
    """
    def setUp(self):
        self.transactions = {
            1: {"merchant_name": "Walmart", "amount": 150, "time_completed": "2024-03-06T10:00:00.000Z"},
            2: {"merchant_name": "Starbucks", "amount": 50, "time_completed": "2024-03-07T11:00:00.000Z"},
            3: {"merchant_name": "Uber", "amount": 100, "time_completed": "2024-03-08T12:00:00.000Z"},
        }
        self.ESG_scores = {
            "Walmart Inc": {"environment_score": 400},
            "Starbucks Corp": {"environment_score": 550}
        }

    # TEST FUZZY MATCHING
    @patch("map.calculations.process.extractOne")
    def test_get_closest_match_walmart(self, mock_extractOne):
        # Test matching "Walmart" to "Walmart Inc" in ESG_scores
        mock_extractOne.return_value = ("Walmart Inc", 90)
        result = _get_closest_match("Walmart", self.ESG_scores)
        self.assertEqual(result, "Walmart Inc")
        mock_extractOne.assert_called_once_with("Walmart", self.ESG_scores)
    
    @patch("map.calculations.process.extractOne")
    def test_get_closest_match_starbucks(self, mock_extractOne):
        # Test matching "Starbucks" to "Starbucks Corp"
        mock_extractOne.return_value = ("Starbucks Corp", 90)
        result = _get_closest_match("Starbucks", self.ESG_scores)
        self.assertEqual(result, "Starbucks Corp")
        mock_extractOne.assert_called_once_with("Starbucks", self.ESG_scores)
    
    @patch("map.calculations.process.extractOne")
    def test_get_closest_match_no_match(self, mock_extractOne):
        # Test when there's no match
        mock_extractOne.return_value = None
        result = _get_closest_match("Uber", self.ESG_scores)
        self.assertEqual(result, None)
        mock_extractOne.assert_called_once_with("Uber", self.ESG_scores)

    def test_company_tier(self):
        # Test all companies return correct tier information given ESG scores. 
        self.assertEqual(_company_tier(244), 4)
        self.assertEqual(_company_tier(245), 4)
        self.assertEqual(_company_tier(500), 4)
        self.assertEqual(_company_tier(501), 3)
        self.assertEqual(_company_tier(520), 3)
        self.assertEqual(_company_tier(521), 2)
        self.assertEqual(_company_tier(600), 1)