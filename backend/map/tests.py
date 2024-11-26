from django.test import TestCase 
from django.urls import reverse 
from unittest.mock import patch, MagicMock 
from django.http import JsonResponse 
import json 
from map.views import get_map_data
from map.use_cases import MapUseCase
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from datetime import datetime, timedelta

from map.env_impact_history import (
    _get_closest_match, 
    _get_company_env_score,
    get_score,
    get_ESG_score_of_transaction_companies, 
    _is_green, 
    get_total_green_transactions, 
    _company_tier, 
    get_most_purchased_companies, 
    _get_start_end_dates, 
    _increment_current_date, 
    calculate_historical_scores,
    _count_green_transactions_in_period, 
    calculate_historical_green_transactions, 
    _get_unique_companies, 
    companies_in_each_tier
)

# test views.py and use_case.py 
class ViewsTestCase(TestCase): 
    """
    Test map.view.  
    """

    def setUp(self):
        # the mock data for testing 
        self.user_id = '0'

    @patch('map.use_cases.MapUseCase.get_user_all_locations_and_company')
    def test_map_use_case(self, mock_get_user_all_locations_and_company):
        """
        Test that MapUseCase returns the correct information. 
        """
        user_map = MapUseCase(self.user_id)
        expected_map_data = [{"location": (88.26035, 75.466192), "merchant_name": "Uber", "merchant_percentile": 3}, {"location": (17.020551, -57.127564), "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": (-75.633331, 2.958381), "merchant_name": "Uber", "merchant_percentile": 3}, {"location": (-72.846083, 169.547942), "merchant_name": "Starbucks", "merchant_percentile": 4}, {"location": (-51.878229, -79.332151), "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": (39.796356, 167.669685), "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": (-71.475794, -161.115052), "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": (60.900455, 78.617571), "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": (-62.94921, 175.384574), "merchant_name": "Starbucks", "merchant_percentile": 4}, {"location": (-11.93821, 76.812633), "merchant_name": "Lyft", "merchant_percentile": 3}, {"location": (-38.710865, -11.936035), "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": (3.648657, 8.686896), "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": (25.936513, -58.436286), "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": (-29.749457, 73.136477), "merchant_name": "Uber", "merchant_percentile": 3}, {"location": (5.866038, -118.725815), "merchant_name": "Target", "merchant_percentile": 2}, {"location": (2.174002, 145.897031), "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": (-4.047713, -65.173013), "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": (79.00523, -97.385509), "merchant_name": "Target", "merchant_percentile": 2}, {"location": (-81.345784, 126.140238), "merchant_name": "Uber", "merchant_percentile": 3}, {"location": (22.330367, -71.485464), "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": (-26.476566, -31.799165), "merchant_name": "Lyft", "merchant_percentile": 3}, {"location": (44.783912, 81.293886), "merchant_name": "Uber", "merchant_percentile": 3}, {"location": (71.497947, -6.378674), "merchant_name": "Uber", "merchant_percentile": 3}, {"location": (-65.597454, 88.731136), "merchant_name": "Target", "merchant_percentile": 2}, {"location": (-6.997066, 159.941119), "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": (-34.022381, -47.734434), "merchant_name": "Target", "merchant_percentile": 2}, {"location": (-21.559461, 136.612372), "merchant_name": "Starbucks", "merchant_percentile": 4}, {"location": (32.544367, 101.548583), "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": (55.265151, 45.007168), "merchant_name": "Uber", "merchant_percentile": 3}, {"location": (6.729, -81.175932), "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": (-29.104179, -158.636863), "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": (23.378072, 37.330195), "merchant_name": "Starbucks", "merchant_percentile": 4}, {"location": (-78.179121, 129.175719), "merchant_name": "Uber", "merchant_percentile": 3}, {"location": (-4.102659, 93.199236), "merchant_name": "Starbucks", "merchant_percentile": 4}, {"location": (-87.104728, 163.811977), "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": (42.358936, -122.681122), "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": (80.718744, 150.235162), "merchant_name": "Uber", "merchant_percentile": 3}, {"location": (52.861278, 108.778184), "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": (71.058645, 39.251017), "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": (29.400995, 178.104457), "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": (73.929604, -81.605588), "merchant_name": "Lyft", "merchant_percentile": 3}]
        mock_get_user_all_locations_and_company.return_value = expected_map_data
        actual_map_data = user_map.get_user_all_locations_and_company()
        self.assertEqual(actual_map_data, expected_map_data)
    

    @patch("map.views.get_map_data")
    def test_get_map_data(self, mock_get_map_data):
        """
        Test that get_map_data returns the correct information given a response.
        """
        request = RequestFactory().get('map/get_map_data/')
        request = add_session_to_request(request)
        request.session['user_id'] = '0' # adding session in manually 
        response = get_map_data(request)
        self.assertIsInstance(response, JsonResponse)
        expected_map_data = [{"location": [88.26035, 75.466192], "merchant_name": "Uber", "merchant_percentile": 3}, {"location": [17.020551, -57.127564], "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": [-75.633331, 2.958381], "merchant_name": "Uber", "merchant_percentile": 3}, {"location": [-72.846083, 169.547942], "merchant_name": "Starbucks", "merchant_percentile": 4}, {"location": [-51.878229, -79.332151], "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": [39.796356, 167.669685], "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": [-71.475794, -161.115052], "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": [60.900455, 78.617571], "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": [-62.94921, 175.384574], "merchant_name": "Starbucks", "merchant_percentile": 4}, {"location": [-11.93821, 76.812633], "merchant_name": "Lyft", "merchant_percentile": 3}, {"location": [-38.710865, -11.936035], "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": [3.648657, 8.686896], "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": [25.936513, -58.436286], "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": [-29.749457, 73.136477], "merchant_name": "Uber", "merchant_percentile": 3}, {"location": [5.866038, -118.725815], "merchant_name": "Target", "merchant_percentile": 2}, {"location": [2.174002, 145.897031], "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": [-4.047713, -65.173013], "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": [79.00523, -97.385509], "merchant_name": "Target", "merchant_percentile": 2}, {"location": [-81.345784, 126.140238], "merchant_name": "Uber", "merchant_percentile": 3}, {"location": [22.330367, -71.485464], "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": [-26.476566, -31.799165], "merchant_name": "Lyft", "merchant_percentile": 3}, {"location": [44.783912, 81.293886], "merchant_name": "Uber", "merchant_percentile": 3}, {"location": [71.497947, -6.378674], "merchant_name": "Uber", "merchant_percentile": 3}, {"location": [-65.597454, 88.731136], "merchant_name": "Target", "merchant_percentile": 2}, {"location": [-6.997066, 159.941119], "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": [-34.022381, -47.734434], "merchant_name": "Target", "merchant_percentile": 2}, {"location": [-21.559461, 136.612372], "merchant_name": "Starbucks", "merchant_percentile": 4}, {"location": [32.544367, 101.548583], "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": [55.265151, 45.007168], "merchant_name": "Uber", "merchant_percentile": 3}, {"location": [6.729, -81.175932], "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": [-29.104179, -158.636863], "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": [23.378072, 37.330195], "merchant_name": "Starbucks", "merchant_percentile": 4}, {"location": [-78.179121, 129.175719], "merchant_name": "Uber", "merchant_percentile": 3}, {"location": [-4.102659, 93.199236], "merchant_name": "Starbucks", "merchant_percentile": 4}, {"location": [-87.104728, 163.811977], "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": [42.358936, -122.681122], "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": [80.718744, 150.235162], "merchant_name": "Uber", "merchant_percentile": 3}, {"location": [52.861278, 108.778184], "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": [71.058645, 39.251017], "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": [29.400995, 178.104457], "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": [73.929604, -81.605588], "merchant_name": "Lyft", "merchant_percentile": 3}]
        mock_get_map_data.return_value = expected_map_data
        actual_map_data = json.loads(response.content)
        self.assertEqual(expected_map_data, actual_map_data)


def add_session_to_request(request):
    """
    Adding session to mock request. 
    """
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()
    return request

# Test env_impact_history.py 
class EnvHistoryTest(TestCase):
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
    @patch("env_impact_history.process.extractOne")
    def test_get_closest_match(self, mock_extractOne):
        # Test matching "Walmart" to "Walmart Inc" in ESG_scores
        mock_extractOne.return_value = ("Walmart Inc", 90)
        result = _get_closest_match("Walmart", self.ESG_scores)
        self.assertEqual(result, "Walmart Inc")
        mock_extractOne.assert_called_once_with("Walmart", self.ESG_scores.keys())
    
    @patch("env_impact_history.process.extractOne")
    def test_get_closest_match(self, mock_extractOne):
        # Test matching "Starbucks" to "Starbucks Corp"
        mock_extractOne.return_value = ("Starbucks Corp", 90)
        result = get_closest_match("Starbucks", self.ESG_scores)
        self.assertEqual(result, "Starbucks Corp")
        mock_extractOne.assert_called_once_with("Starbucks", self.ESG_scores.keys())
    
    @patch("env_impact_history.process.extractOne")
    def test_get_closest_match(self, mock_extractOne):
        # Test when there's no match
        mock_extractOne.return_value = None
        result = _get_closest_match("Uber", self.ESG_scores)
        self.assertEqual(result, None)
        mock_extractOne.assert_called_once_with("Starbucks", self.ESG_scores.keys())

    # TEST COMPANY ENV SCORE
    @patch("env_impact_history.get_closest_match")
    def test_get_company_env_score(self, mock_get_closest_match):
        mock_get_closest_match.return_value = "Walmart Inc"
        transaction = {"merchant_name": "Walmart"}
        result = _get_company_env_score(transaction, self.ESG_scores)
        self.assertEqual(result, 400)

        mock_get_closest_match.return_value = "Starbucks Corp"
        transaction = {"merchant_name": "Starbucks"}
        result = _get_company_env_score(transaction, self.ESG_scores)
        self.assertEqual(result, 550)
        
        # Test matching with "Uber" which should have no match
        mock_get_closest_match.return_value = None
        transaction = {"merchant_name": "Uber"}
        result = _get_company_env_score(transaction, self.ESG_scores)
        self.assertEqual(result, 0)


    # TEST CARBON SCORE
    @patch("env_impact_history.get_company_env_score")
    def test_get_score(self, mock_get_company_env_score):
        mock_get_company_env_score.side_effect = [400, 550, 0]
        start = datetime(2024, 3, 5)
        end = datetime(2024, 3, 8)
        result = get_score(self.transactions, start, end, self.ESG_scores)
        self.assertAlmostEqual(result, 466.67, places=1)  # Weighted average of the scores
    
    @patch("env_impact_history.get_company_env_score")
    def test_get_ESG_score_of_transaction_companies(self, mock_get_company_env_score):
        mock_get_company_env_score.side_effect = [400, 550, 0]
        result = get_ESG_score_of_transaction_companies(self.transactions.values(), self.ESG_scores)
        expected = [{"Walmart": 400}, {"Starbucks": 550}, {"Uber": 0}]
        self.assertEqual(result, expected)
    
    @patch("env_impact_history.get_company_env_score")
    def test_get_total_green_transactions(self, mock_get_company_env_score):
        mock_get_company_env_score.side_effect = [400, 550, 0]
        result = get_total_green_transactions(self.transactions.values(), self.ESG_scores)
        self.assertEqual(result, 1)  # Only Starbucks meets the threshold of 500

    @patch("env_impact_history.get_company_env_score")
    def test_get_most_purchased_companies(self, mock_get_company_env_score):
        transactions = [
            {"merchant_name": "Walmart", "amount": 150},
            {"merchant_name": "Starbucks", "amount": 50},
            {"merchant_name": "Uber", "amount": 100},
        ]
        mock_get_company_env_score.side_effect = [400, 550, 0]
        result = get_most_purchased_companies(transactions, self.ESG_scores)
        expected = [
            {"Company Name": "Walmart", "ESG Score": 400, "Amount Spent": 150},
            {"Company Name": "Uber", "ESG Score": 0, "Amount Spent": 100},
            {"Company Name": "Starbucks", "ESG Score": 550, "Amount Spent": 50},
        ]
        self.assertEqual(result, expected)

    def test_get_user_transactions(self):
        all_transactions = {
            1: {"customerID": 1, "merchant_name": "Walmart", "amount": 150},
            2: {"customerID": 2, "merchant_name": "Starbucks", "amount": 50},
        }
        user_transactions = get_user_transactions(all_transactions, 1)
        expected = {1: {"customerID": 1, "merchant_name": "Walmart", "amount": 150}}
        self.assertEqual(user_transactions, expected)
    
    def test_get_start_end_dates_weekly(self):
        current_date = datetime(2024, 3, 7)  # Thursday
        start_date, end_date = _get_start_end_dates("weekly", current_date)
        expected_start = datetime(2024, 3, 4)  # Monday
        expected_end = datetime(2024, 3, 10)  # Sunday
        self.assertEqual(start_date, expected_start)
        self.assertEqual(end_date, expected_end)

    def test_get_start_end_dates_monthly(self):
        current_date = datetime(2024, 3, 15)
        start_date, end_date = _get_start_end_dates("monthly", current_date)
        expected_start = datetime(2024, 3, 1)
        expected_end = datetime(2024, 3, 31)
        self.assertEqual(start_date, expected_start)
        self.assertEqual(end_date, expected_end)

    @patch("env_impact_history.get_score")
    def test_calculate_historical_scores(self, mock_get_score):
        mock_get_score.side_effect = [100, 200, 300]  # Mocked scores
        current_date = datetime(2024, 3, 15)
        user_transactions = MagicMock()
        esg_scores = MagicMock()
        result = calculate_historical_scores("weekly", current_date, user_transactions, esg_scores)
        self.assertEqual(result[:3], [100, 200, 300])  # Check first three results
    
    def test_company_tier(self):
        self.assertEqual(company_tier(244), 4)
        self.assertEqual(company_tier(245), 3)
        self.assertEqual(company_tier(500), 3)
        self.assertEqual(company_tier(501), 2)
        self.assertEqual(company_tier(520), 2)
        self.assertEqual(company_tier(521), 1)
    