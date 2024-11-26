from django.test import TestCase 
from unittest.mock import patch
from map.calculations import (
    _get_closest_match, 
    _company_tier, 
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