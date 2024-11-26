import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from .env_impact_history import (
    get_closest_match,
    get_company_env_score,
    get_score,
    get_ESG_score_of_transaction_companies,
    get_total_green_transactions,
    get_most_purchased_companies,
    get_user_transactions,
    _get_start_end_dates,
    calculate_historical_scores,
)

class TestFunctions(unittest.TestCase):
    # FAKE THE DICTIONARIES
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
        result = get_closest_match("Walmart", self.ESG_scores)
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
        result = get_closest_match("Uber", self.ESG_scores)
        self.assertEqual(result, None)
        mock_extractOne.assert_called_once_with("Starbucks", self.ESG_scores.keys())

    # TEST COMPANY ENV SCORE
    @patch("env_impact_history.get_closest_match")
    def test_get_company_env_score(self, mock_get_closest_match):
        mock_get_closest_match.return_value = "Walmart Inc"
        transaction = {"merchant_name": "Walmart"}
        result = get_company_env_score(transaction, self.ESG_scores)
        self.assertEqual(result, 400)

        mock_get_closest_match.return_value = "Starbucks Corp"
        transaction = {"merchant_name": "Starbucks"}
        result = get_company_env_score(transaction, self.ESG_scores)
        self.assertEqual(result, 550)
        
        # Test matching with "Uber" which should have no match
        mock_get_closest_match.return_value = None
        transaction = {"merchant_name": "Uber"}
        result = get_company_env_score(transaction, self.ESG_scores)
        self.assertEqual(result, 0)

    # UNEDITED CHATGPT TESTS

    # TEST CARBON SCORE
    # this is just generated by chatgpt i didn't calculate it so it's prob failing cuz test is wrong
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
    
if __name__ == "__main__":
    unittest.main()