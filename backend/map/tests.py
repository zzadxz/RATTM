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
from map.use_cases import MapUseCase
from utils.abstract_data_access import AbstractDataAccess

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


class UseCaseTest(TestCase):
    """
    Tests for MapUseCase.
    """

    def setUp(self):
        # Create a mock for AbstractDataAccess
        self.mock_data_access = MagicMock(spec=AbstractDataAccess)
        # Initialize MapUseCase with the mock data access
        self.use_case = MapUseCase(data_access=self.mock_data_access)
"""

    @patch('map.use_cases._get_closest_match', return_value='Walmart Inc')
    @patch('map.use_cases._company_tier', return_value=4)
    def test_get_user_all_locations_and_company(self, mock_company_tier, mock_get_closest_match):
        # Mock data
        user_id = '123'
        user_transactions = [
            {'merchant_name': 'Walmart', 'latitude': 40.7128, 'longitude': -74.0060}
        ]
        esg_data = {'Walmart Inc': {'environment_score': 400}}

        # Mock `get_table_from_database`
        self.mock_data_access.get_table_from_database.side_effect = [
            {'123': {'transactions': user_transactions}},  # User transactions
            esg_data                                      # ESG data
        ]

        # Call the function
        result = self.use_case.get_user_all_locations_and_company(user_id)

        # Expected result
        expected_result = [
            {
                "location": (40.7128, -74.0060),
                "merchant_name": "Walmart",
                "merchant_percentile": 4,
            }
        ]

        # Assert the output matches the expected result
        self.assertEqual(result, expected_result)

    def test_get_user_all_locations_and_company_no_transactions(self):
        #Test that MapUseCase.get_user_all_locations_and_company handles users with no transactions.

        user_id = '456'
        user_transactions = []
        esg_data = {}

        # Mock the data_access.get_table_from_database method
        self.mock_data_access.get_table_from_database.side_effect = [
            {'456': {'transactions': user_transactions}},  # First call returns empty transactions
            esg_data                                       # Second call returns empty ESG data
        ]

        # Call the method under test
        result = self.use_case.get_user_all_locations_and_company(user_id)

        expected_result = []

        # Assert that the result is an empty list
        self.assertEqual(result, expected_result)

        # Verify that data_access.get_table_from_database was called twice
        self.assertEqual(self.mock_data_access.get_table_from_database.call_count, 2)
        self.mock_data_access.get_table_from_database.assert_any_call('Users')
        self.mock_data_access.get_table_from_database.assert_any_call('esg')
"""

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

class AbstractUseCaseTest(TestCase):
    """
    Test to ensure AbstractMapUseCase enforces the required interface methods.
    """

    def test_cannot_instantiate_abstract_class(self):
        """
        Ensure that attempting to instantiate AbstractMapUseCase raises a TypeError.
        """
        with self.assertRaises(TypeError):
            AbstractMapUseCase()

    def test_complete_concrete_implementation(self):
        """
        Ensure a complete implementation of AbstractMapUseCase works without errors.
        """

        class TestConcreteMapUseCase(AbstractMapUseCase):
            """
            A dummy implementation to validate the abstract class.
            """
            def __init__(self):
                pass

            def get_user_all_locations_and_company(self, user_id):
                return [{"location": (40.7128, -74.0060), "merchant_name": "Test Merchant"}]

        # Ensure no errors when instantiating and using the concrete class
        test_instance = TestConcreteMapUseCase()
        result = test_instance.get_user_all_locations_and_company("123")
        self.assertEqual(
            result,
            [{"location": (40.7128, -74.0060), "merchant_name": "Test Merchant"}],
        )

    def test_incomplete_implementation(self):
        """
        Ensure an incomplete implementation raises TypeError when instantiated.
        """

        class IncompleteMapUseCase(AbstractMapUseCase):
            """
            A deliberately incomplete implementation.
            """
            def __init__(self):
                pass

        # Ensure an error is raised due to missing abstract methods
        with self.assertRaises(TypeError):
            IncompleteMapUseCase()

    def test_partial_concrete_implementation_missing_method(self):
        """
        Ensure that an implementation missing 'get_user_all_locations_and_company'
        raises a TypeError.
        """

        class PartialConcreteMapUseCase(AbstractMapUseCase):
            """
            A partial implementation missing one required method.
            """
            def __init__(self):
                pass

        # Attempt to instantiate should raise an error
        with self.assertRaises(TypeError):
            PartialConcreteMapUseCase()