''' This file is used to test the core, important functions in calculations.py and use_cases.py'''

import json
from django.test import TestCase, RequestFactory
from utils.firebase import db
from .calculations import Calculations
from datetime import datetime
from unittest.mock import MagicMock
from .use_case import DashboardUseCases
from utils.abstract_data_access import AbstractDataAccess
from django.http import JsonResponse
from .abstract_use_case import AbstractDashboardUseCases
from .views import DashboardView

"""
class TestCalculations(TestCase):
    def setUp(self):
        self.esg = {
            '3M Co': {'environment_score': 526},
            'A O Smith Corp': {'environment_score': 510},
            'Green Company': {'environment_score': 570},
            'Borderline Company': {'environment_score': 490},
        }
        self.transactions = [
            {'merchant_name': '3M Co', 'amount': 860.27, 'time_completed': '2024-01-15T12:00:00.000Z'},
            {'merchant_name': 'A O Smith Corp', 'amount': 144.53, 'time_completed': '2024-01-10T12:00:00.000Z'},
            {'merchant_name': 'Green Company', 'amount': 500.00, 'time_completed': '2024-01-05T12:00:00.000Z'},
            {'merchant_name': 'Borderline Company', 'amount': 250.00, 'time_completed': '2024-01-01T12:00:00.000Z'},
        ]
        self.calc = Calculations()

    def test_get_closest_match(self):
        #"Test _get_closest_match."
        result = self.calc._get_closest_match("3M", self.esg)
        self.assertEqual(result, "3M Co")

        result = self.calc._get_closest_match("Smith Corp", self.esg)
        self.assertEqual(result, "A O Smith Corp")

        result = self.calc._get_closest_match("Unknown Corp", self.esg)
        self.assertIsNone(result)

    def test_get_company_env_score(self):
        #Test _get_company_env_score.
        transaction = {'merchant_name': '3M Co'}
        self.assertEqual(self.calc._get_company_env_score(transaction, self.esg), 526)

        transaction = {'merchant_name': 'Unknown Corp'}
        self.assertEqual(self.calc._get_company_env_score(transaction, self.esg), 0)

    def test_is_green(self):
        #Test _is_green.
        transaction = {'merchant_name': '3M Co'}
        self.assertTrue(self.calc._is_green(transaction, self.esg))

        transaction = {'merchant_name': 'Borderline Company'}
        self.assertFalse(self.calc._is_green(transaction, self.esg))

    def test_company_tier(self):
        #Test _company_tier.
        self.assertEqual(self.calc._company_tier(570), 1)
        self.assertEqual(self.calc._company_tier(530), 2)
        self.assertEqual(self.calc._company_tier(510), 3)
        self.assertEqual(self.calc._company_tier(490), 4)

    def test_get_start_end_dates(self):
        #Test _get_start_end_dates.
        current_date = datetime(2024, 1, 15)
        start_date, end_date = self.calc._get_start_end_dates(current_date)
        self.assertEqual(start_date, datetime(2024, 1, 1))
        self.assertEqual(end_date, datetime(2024, 1, 31))

    def test_count_green_transactions_in_period(self):
        #Test _count_green_transactions_in_period.
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 1, 31)
        result = self.calc._count_green_transactions_in_period(self.transactions, start_date, end_date, self.esg)
        self.assertEqual(result, 3)

    def test_get_unique_companies(self):
        #Test _get_unique_companies
        result = self.calc._get_unique_companies(self.transactions, self.esg)
        self.assertEqual(result, {'3M Co', 'A O Smith Corp', 'Green Company', 'Borderline Company'})

    def test_calculate_score(self):
        #Test calculate_score
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 1, 31)
        score = self.calc.calculate_score(self.transactions, start_date, end_date, self.esg)
        self.assertEqual(score, 532)

    def test_calculate_score_no_transactions(self):
        #Test calculate_score with no transactions in the date range
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 1, 31)
        score = self.calc.calculate_score(self.transactions, start_date, end_date, self.esg)
        self.assertIsNone(score)

    def test_calculate_company_esg_scores(self):
        #Test calculate_company_esg_scores
        scores = self.calc.calculate_company_esg_scores(self.transactions, self.esg)
        expected_scores = [
            {'3M Co': 526},
            {'A O Smith Corp': 510},
            {'Green Company': 570},
            {'Borderline Company': 490},
        ]
        self.assertEqual(scores, expected_scores)

    def test_calculate_total_green_transactions(self):
        #Test calculate_total_green_transactions
        total_green = self.calc.calculate_total_green_transactions(self.transactions, self.esg)
        self.assertEqual(total_green, 3)

    def test_find_most_purchased_companies(self):
        #Test find_most_purchased_companies
        top_companies = self.calc.find_most_purchased_companies(self.transactions, self.esg)
        expected_top_companies = [
            {'Company Name': '3M Co', 'ESG Score': 526, 'Amount Spent': 860.27},
            {'Company Name': 'Green Company', 'ESG Score': 570, 'Amount Spent': 500.00},
            {'Company Name': 'Borderline Company', 'ESG Score': 490, 'Amount Spent': 250.00},
            {'Company Name': 'A O Smith Corp', 'ESG Score': 510, 'Amount Spent': 144.53},
        ]
        self.assertEqual(top_companies, expected_top_companies)

    def test_calculate_historical_scores(self):
        #Test calculate_historical_scores
        historical_scores = self.calc.calculate_historical_scores(self.transactions, self.esg)
        self.assertEqual(len(historical_scores), 12)

    def test_calculate_historical_green_transactions(self):
        #Test calculate_historical_green_transactions
        historical_green_transactions = self.calc.calculate_historical_green_transactions(self.transactions, self.esg)
        self.assertEqual(len(historical_green_transactions), 12)

    def test_find_companies_in_each_tier(self):
        #Test find_companies_in_each_tier
        tier_counts = self.calc.find_companies_in_each_tier(self.transactions, self.esg)
        self.assertEqual(tier_counts, [1, 1, 1, 1])

class TestUseCases(TestCase):
    def setUp(self):
        self.mock_calculations = MagicMock(spec=Calculations)
        self.mock_data_access = MagicMock(spec=AbstractDataAccess)
        self.use_cases = DashboardUseCases(self.mock_calculations, self.mock_data_access)

        self.user_id = "test_user"
        self.mock_transactions = [
            {"merchant_name": "CompanyA", "amount": 100, "time_completed": "2023-01-01T12:00:00Z"},
            {"merchant_name": "CompanyB", "amount": 200, "time_completed": "2023-02-01T12:00:00Z"},
        ]
        self.mock_esg_data = {
            "CompanyA": {"environment_score": 500},
            "CompanyB": {"environment_score": 450},
        }

        # Mock return values for data access
        self.mock_data_access.get_table_from_database.side_effect = lambda table: {
            "Users": {self.user_id: {"transactions": self.mock_transactions}},
            "esg": self.mock_esg_data,
        }.get(table)

    def test_past_12_month_names(self):
        #Test the past_12_month_names method
        expected_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        result = self.use_cases.past_12_month_names()
        self.assertEqual(len(result), 12, "Should return 12 months")
        self.assertTrue(all(month in expected_months for month in result), "All months should be valid")

    def test_monthly_carbon_scores(self):
        #Test the monthly_carbon_scores method
        self.mock_calculations.calculate_historical_scores.return_value = [100, 200, 300]
        result = self.use_cases.monthly_carbon_scores(self.user_id)
        self.assertEqual(result, [300, 200, 100], "Should return reversed carbon scores")
        self.mock_calculations.calculate_historical_scores.assert_called_once_with(
            self.mock_transactions, self.mock_esg_data
        )

    def test_monthly_green_transactions(self):
        #Test the monthly_green_transactions method
        self.mock_calculations.calculate_historical_green_transactions.return_value = [1, 2, 3]
        result = self.use_cases.monthly_green_transactions(self.user_id)
        self.assertEqual(result, [3, 2, 1], "Should return reversed green transaction counts")
        self.mock_calculations.calculate_historical_green_transactions.assert_called_once_with(
            self.mock_transactions, self.mock_esg_data
        )

    def test_total_green_transactions(self):
        #Test the total_green_transactions method
        self.mock_calculations.calculate_total_green_transactions.return_value = 10
        result = self.use_cases.total_green_transactions(self.user_id)
        self.assertEqual(result, 10, "Should return total green transactions")
        self.mock_calculations.calculate_total_green_transactions.assert_called_once_with(
            self.mock_transactions, self.mock_esg_data
        )

    def test_this_month_green_transactions(self):
        #Test the this_month_green_transactions method
        self.mock_calculations.calculate_historical_green_transactions.return_value = [5, 3, 2]
        result = self.use_cases.this_month_green_transactions(self.user_id)
        self.assertEqual(result, 5, "Should return green transactions for this month")
        self.mock_calculations.calculate_historical_green_transactions.assert_called_once_with(
            self.mock_transactions, self.mock_esg_data
        )

    def test_top_5_companies(self):
        #Test the top_5_companies method
        expected_result = {"CompanyA": {"ESG Score": 500, "Amount Spent": 100}}
        self.mock_calculations.find_most_purchased_companies.return_value = expected_result
        result = self.use_cases.top_5_companies(self.user_id)
        self.assertEqual(result, expected_result, "Should return top 5 companies")
        self.mock_calculations.find_most_purchased_companies.assert_called_once_with(
            self.mock_transactions, self.mock_esg_data
        )

    def test_total_co2_score(self):
        #Test the total_co2_score method
        self.mock_calculations.calculate_historical_scores.return_value = [500, 400, 300]
        result = self.use_cases.total_co2_score(self.user_id)
        self.assertEqual(result, 400, "Should return average CO2 score")
        self.mock_calculations.calculate_historical_scores.assert_called_once_with(
            self.mock_transactions, self.mock_esg_data
        )

    def test_this_month_co2_score(self):
        #Test the this_month_co2_score method
        self.mock_calculations.calculate_historical_scores.return_value = [400, 300, 200]
        result = self.use_cases.this_month_co2_score(self.user_id)
        self.assertEqual(result, 400, "Should return CO2 score for this month")
        self.mock_calculations.calculate_historical_scores.assert_called_once_with(
            self.mock_transactions, self.mock_esg_data
        )

    def test_company_tiers(self):
        #Test the company_tiers method
        expected_tiers = [5, 3, 2, 1]
        self.mock_calculations.find_companies_in_each_tier.return_value = expected_tiers
        result = self.use_cases.company_tiers(self.user_id)
        self.assertEqual(result, expected_tiers, "Should return the number of companies in each tier")
        self.mock_calculations.find_companies_in_each_tier.assert_called_once_with(
            self.mock_transactions, self.mock_esg_data
        )

    def test_co2_score_change(self):
        #Test the co2_score_change method
        self.mock_calculations.calculate_historical_scores.return_value = [500, 450]
        result = self.use_cases.co2_score_change(self.user_id)
        self.assertEqual(result, 50, "Should return the change in CO2 score")
        self.mock_calculations.calculate_historical_scores.assert_called_once_with(
            self.mock_transactions, self.mock_esg_data
        )

    def test_green_transaction_change(self):
        #Test the green_transaction_change method
        self.mock_calculations.calculate_historical_green_transactions.return_value = [10, 7]
        result = self.use_cases.green_transaction_change(self.user_id)
        self.assertEqual(result, 3, "Should return the change in green transactions")
        self.mock_calculations.calculate_historical_green_transactions.assert_called_once_with(
            self.mock_transactions, self.mock_esg_data
        )

class ViewTests(TestCase):
    #
    #Tests for DashboardView and its interaction with AbstractDashboardUseCases.
    

    def setUp(self):
        # Mock use case dependency
        self.mock_use_cases = MagicMock(spec=AbstractDashboardUseCases)
        self.view = DashboardView(self.mock_use_cases)
        self.factory = RequestFactory()

    def _setup_request_with_session(self, session_data=None):
        """
        #Helper function to create a mock request with session data.
        """
        request = self.factory.get("/dashboard/data/")
        request.session = session_data or {}
        return request

    def parse_json_response(self, response):
        """
        #Helper to parse a JsonResponse into a Python object.
        """
        return json.loads(response.content.decode('utf-8'))

    def test_get_line_graph_data(self):
        """
        #Test get_line_graph_data method.
        """
        # Mock return values
        self.mock_use_cases.past_12_month_names.return_value = ["Jan", "Feb", "Mar"]
        self.mock_use_cases.monthly_carbon_scores.return_value = [100, 200, 300]
        self.mock_use_cases.monthly_green_transactions.return_value = [10, 20, 30]

        # Setup request with session
        request = self._setup_request_with_session({"user_id": "123"})

        # Call the method
        response = self.view.get_line_graph_data(request)

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        parsed_response = self.parse_json_response(response)
        self.assertEqual(
            parsed_response,
            {
                "months": ["Jan", "Feb", "Mar"],
                "carbon_scores": [100, 200, 300],
                "green_transactions": [10, 20, 30],
            },
        )
        self.mock_use_cases.past_12_month_names.assert_called_once()
        self.mock_use_cases.monthly_carbon_scores.assert_called_once_with("123")
        self.mock_use_cases.monthly_green_transactions.assert_called_once_with("123")

    def test_get_total_green_transactions(self):
        """
        #Test get_total_green_transactions method.
        """
        self.mock_use_cases.total_green_transactions.return_value = 50

        request = self._setup_request_with_session({"user_id": "123"})
        response = self.view.get_total_green_transactions(request)

        self.assertIsInstance(response, JsonResponse)
        parsed_response = self.parse_json_response(response)
        self.assertEqual(parsed_response, 50)
        self.mock_use_cases.total_green_transactions.assert_called_once_with("123")

    def test_get_total_co2_score(self):
        """
        #Test the total CO2 score retrieval.
        """
        self.mock_use_cases.total_co2_score.return_value = 1000

        request = self._setup_request_with_session({"user_id": "123"})
        response = self.view.get_total_co2_score(request)

        self.assertIsInstance(response, JsonResponse)
        parsed_response = self.parse_json_response(response)
        self.assertEqual(parsed_response, 1000)
        self.mock_use_cases.total_co2_score.assert_called_once_with("123")

    def test_get_company_tiers(self):
        """
        #Test get_company_tiers method.
        """
        tiers = [5, 3, 2, 1]
        self.mock_use_cases.company_tiers.return_value = tiers

        request = self._setup_request_with_session({"user_id": "123"})
        response = self.view.get_company_tiers(request)

        self.assertIsInstance(response, JsonResponse)
        parsed_response = self.parse_json_response(response)
        self.assertEqual(parsed_response, tiers)
        self.mock_use_cases.company_tiers.assert_called_once_with("123")

    def test_get_green_transaction_change(self):
        """
        #Test the green transaction change retrieval.
        """
        self.mock_use_cases.green_transaction_change.return_value = 20

        request = self._setup_request_with_session({"user_id": "123"})
        response = self.view.get_green_transaction_change(request)

        self.assertIsInstance(response, JsonResponse)
        parsed_response = self.parse_json_response(response)
        self.assertEqual(parsed_response, 20)
        self.mock_use_cases.green_transaction_change.assert_called_once_with("123")
"""
