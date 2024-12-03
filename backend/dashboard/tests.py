''' This file is used to test the core, important functions in calculations.py and use_cases.py'''

from django.test import TestCase
from utils.firebase import db
from .calculations import Calculations
from datetime import datetime
from unittest.mock import MagicMock
from .use_case import DashboardUseCases
from utils.abstract_data_access import AbstractDataAccess


class TestCalculations(TestCase):
    def setUp(self):
        # FAKE THE DICTIONARIES
        self.esg = {'3M Co': {'environment_level': 'High', 'social_grade': 'BB', 
                              'governance_level': 'Medium', 'social_level': 'Medium', 
                              'total_score': 1141, 'total_grade': 'BBB', 'social_score': 310, 
                              'weburl': 'https://www.3m.com/', 'exchange': 'NEW YORK STOCK EXCHANGE, INC.', 
                              'cik': 66740, 'logo': 'https://static.finnhub.io/logo/2a1802fa-80ec-11ea-a0f5-00000000092a.png', 
                              'industry': 'Industrial Conglomerates', 'governance_score': 305, 
                              'total_level': 'High', 'currency': 'USD', 'governance_grade': 'BB', 
                              'environment_score': 526, 'last_processing_date': '16-04-2022', 
                              'environment_grade': 'A', 'ticker': 'mmm'}, 
                    'A O Smith Corp': {'environment_level': 'High', 'social_grade': 'BB',
                                        'governance_level': 'Medium', 'social_level': 'Medium', 
                                        'total_score': 1135, 'total_grade': 'BBB', 'social_score': 315, 
                                        'weburl': 'https://www.aosmith.com/', 'exchange': 'NEW YORK STOCK EXCHANGE, INC.', 
                                        'cik': 91142, 'logo': 'https://static.finnhub.io/logo/73381be8-80eb-11ea-b385-00000000092a.png', 
                                        'industry': 'Building', 'governance_score': 310, 'total_level': 'High', 
                                        'currency': 'USD', 'governance_grade': 'BB', 'environment_score': 510, 
                                        'last_processing_date': '16-04-2022', 'environment_grade': 'A', 'ticker': 'aos'}}
        
        self.transactions = [{'action': 'declined', 'time_completed': '2024-08-31T06:02:27.687Z', 
                                   'longitude': -113.807658, 'merchant_name': '3M Co', 'latitude': -42.372604, 
                                   'customerID': 52, 'amount': 860.27, 'ip_address': '179.152.194.186'}, 
                             {'action': 'declined', 'time_completed': '2023-12-07T08:07:20.451Z', 
                                   'longitude': -1.121183, 'merchant_name': 'Smith Corp', 'latitude': 11.962175, 
                                   'customerID': 52, 'amount': 144.53, 'ip_address': '173.64.65.25'}]
    def test_get_closest_match(self):
        calc = Calculations()
        # Test matching "3M Co" to "3M Co" in ESG_scores
        result = calc._get_closest_match("3M", self.esg)
        self.assertEqual(result, "3M Co")
        
        # Test matching "Smith Corp" to "A O Smith Corp"
        result = calc._get_closest_match("Smith Corp", self.esg)
        self.assertEqual(result, "A O Smith Corp")
        
        # Test when there's no match
        result = calc._get_closest_match("RATTM Corp", self.esg)
        self.assertEqual(result, None)
        
    def test_get_company_env_score(self):
        calc = Calculations()
        transaction = {"merchant_name": "3M Co"}
        result = calc._get_company_env_score(transaction, self.esg)
        self.assertEqual(result, 526)

        transaction = {"merchant_name": "A O Smith Corp"}
        result = calc._get_company_env_score(transaction, self.esg)
        self.assertEqual(result, 510)
        
        # Test matching with "Uber" which should have no match
        transaction = {"merchant_name": "Uber"}
        result = calc._get_company_env_score(transaction, self.esg)
        self.assertEqual(result, 0)
    
    
    def test_company_tier(self):
        calc = Calculations()
        self.assertEqual(calc._company_tier(600), 1)
        self.assertEqual(calc._company_tier(501), 3)
        
    def test_count_green_transactions_in_period(self):
        calc = Calculations()
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2024, 1, 1)
        result = calc._count_green_transactions_in_period(self.transactions, start_date, end_date, self.esg)
        self.assertEqual(result, 1)
        
    def test_get_unique_companies(self):
        calc = Calculations()
        result = calc._get_unique_companies(self.transactions, self.esg)
        self.assertEqual(result, {"3M Co", "A O Smith Corp"})
    
    
    def test_get_total_green_transactions(self):
        calc = Calculations()
        result = calc.calculate_total_green_transactions(self.transactions, self.esg)
        self.assertEqual(result, 2)
    

class AdditionalCalculationsTest(TestCase):
    def setUp(self):
        # FAKE THE DICTIONARIES
        self.esg = {
            '3M Co': {
                'environment_score': 526,
            }, 
            'A O Smith Corp': {
                'environment_score': 510,
            },
            'Green Company': {
                'environment_score': 570,
            },
            'Borderline Company': {
                'environment_score': 510,
            }
        }
        
        # Create a more diverse set of transactions for comprehensive testing
        self.transactions = [
            {
                'merchant_name': '3M Co', 
                'time_completed': '2024-01-15T12:00:00.000Z', 
                'amount': 860.27
            }, 
            {
                'merchant_name': 'A O Smith Corp', 
                'time_completed': '2024-01-10T12:00:00.000Z', 
                'amount': 144.53
            },
            {
                'merchant_name': 'Green Company', 
                'time_completed': '2024-01-05T12:00:00.000Z', 
                'amount': 500.00
            },
            {
                'merchant_name': 'Borderline Company', 
                'time_completed': '2024-01-01T12:00:00.000Z', 
                'amount': 250.00
            }
        ]

    def test_company_tier_detailed(self):
        """Test the _company_tier function with more detailed scenarios"""
        calc = Calculations()
        self.assertEqual(calc._company_tier(570), 1, "Score above 560 should be tier 1")
        self.assertEqual(calc._company_tier(540), 2, "Score between 520 and 560 should be tier 2")
        self.assertEqual(calc._company_tier(510), 3, "Score between 500 and 520 should be tier 3")
        self.assertEqual(calc._company_tier(490), 4, "Score below 500 should be tier 4")
        
    def test_calculate_historical_green_transactions(self):
        """Test the calculate_historical_green_transactions function"""
        calc = Calculations()
        historical_green_transactions = calc.calculate_historical_green_transactions(self.transactions, self.esg)
        
        # Verify the length of the returned list
        self.assertEqual(len(historical_green_transactions), 12, "Should return green transaction counts for 12 months")
        
        # Verify that the counts are calculated
        self.assertIsNotNone(historical_green_transactions[0], "First month's green transaction count should be calculable")


class TestUseCases(TestCase):
    def setUp(self):
        # Mock dependencies
        self.mock_calculations = MagicMock(spec=Calculations)
        self.mock_data_access = MagicMock(spec=AbstractDataAccess)
        self.use_cases = DashboardUseCases(self.mock_calculations, self.mock_data_access)

        # Mock user data
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
        """Test the past_12_month_names method."""
        expected_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        result = self.use_cases.past_12_month_names()
        self.assertEqual(len(result), 12, "Should return 12 months")
        self.assertTrue(all(month in expected_months for month in result), "All months should be valid")

    def test_monthly_carbon_scores(self):
        """Test the monthly_carbon_scores method."""
        self.mock_calculations.calculate_historical_scores.return_value = [100, 200, 300]
        result = self.use_cases.monthly_carbon_scores(self.user_id)
        self.assertEqual(result, [300, 200, 100], "Should return reversed carbon scores")
        self.mock_calculations.calculate_historical_scores.assert_called_once_with(
            self.mock_transactions, self.mock_esg_data
        )

    def test_monthly_green_transactions(self):
        """Test the monthly_green_transactions method."""
        self.mock_calculations.calculate_historical_green_transactions.return_value = [1, 2, 3]
        result = self.use_cases.monthly_green_transactions(self.user_id)
        self.assertEqual(result, [3, 2, 1], "Should return reversed green transaction counts")
        self.mock_calculations.calculate_historical_green_transactions.assert_called_once_with(
            self.mock_transactions, self.mock_esg_data
        )

    def test_total_green_transactions(self):
        """Test the total_green_transactions method."""
        self.mock_calculations.calculate_total_green_transactions.return_value = 10
        result = self.use_cases.total_green_transactions(self.user_id)
        self.assertEqual(result, 10, "Should return total green transactions")
        self.mock_calculations.calculate_total_green_transactions.assert_called_once_with(
            self.mock_transactions, self.mock_esg_data
        )

    def test_this_month_green_transactions(self):
        """Test the this_month_green_transactions method."""
        self.mock_calculations.calculate_historical_green_transactions.return_value = [5, 3, 2]
        result = self.use_cases.this_month_green_transactions(self.user_id)
        self.assertEqual(result, 5, "Should return green transactions for this month")
        self.mock_calculations.calculate_historical_green_transactions.assert_called_once_with(
            self.mock_transactions, self.mock_esg_data
        )

    def test_top_5_companies(self):
        """Test the top_5_companies method."""
        expected_result = {"CompanyA": {"ESG Score": 500, "Amount Spent": 100}}
        self.mock_calculations.find_most_purchased_companies.return_value = expected_result
        result = self.use_cases.top_5_companies(self.user_id)
        self.assertEqual(result, expected_result, "Should return top 5 companies")
        self.mock_calculations.find_most_purchased_companies.assert_called_once_with(
            self.mock_transactions, self.mock_esg_data
        )

    def test_total_co2_score(self):
        """Test the total_co2_score method."""
        self.mock_calculations.calculate_historical_scores.return_value = [500, 400, 300]
        result = self.use_cases.total_co2_score(self.user_id)
        self.assertEqual(result, 400, "Should return average CO2 score")
        self.mock_calculations.calculate_historical_scores.assert_called_once_with(
            self.mock_transactions, self.mock_esg_data
        )

    def test_this_month_co2_score(self):
        """Test the this_month_co2_score method."""
        self.mock_calculations.calculate_historical_scores.return_value = [400, 300, 200]
        result = self.use_cases.this_month_co2_score(self.user_id)
        self.assertEqual(result, 400, "Should return CO2 score for this month")
        self.mock_calculations.calculate_historical_scores.assert_called_once_with(
            self.mock_transactions, self.mock_esg_data
        )

    def test_company_tiers(self):
        """Test the company_tiers method."""
        expected_tiers = [5, 3, 2, 1]
        self.mock_calculations.find_companies_in_each_tier.return_value = expected_tiers
        result = self.use_cases.company_tiers(self.user_id)
        self.assertEqual(result, expected_tiers, "Should return the number of companies in each tier")
        self.mock_calculations.find_companies_in_each_tier.assert_called_once_with(
            self.mock_transactions, self.mock_esg_data
        )

    def test_co2_score_change(self):
        """Test the co2_score_change method."""
        self.mock_calculations.calculate_historical_scores.return_value = [500, 450]
        result = self.use_cases.co2_score_change(self.user_id)
        self.assertEqual(result, 50, "Should return the change in CO2 score")
        self.mock_calculations.calculate_historical_scores.assert_called_once_with(
            self.mock_transactions, self.mock_esg_data
        )

    def test_green_transaction_change(self):
        """Test the green_transaction_change method."""
        self.mock_calculations.calculate_historical_green_transactions.return_value = [10, 7]
        result = self.use_cases.green_transaction_change(self.user_id)
        self.assertEqual(result, 3, "Should return the change in green transactions")
        self.mock_calculations.calculate_historical_green_transactions.assert_called_once_with(
            self.mock_transactions, self.mock_esg_data
        )
