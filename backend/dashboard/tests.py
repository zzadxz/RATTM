# import sys
# import os

# # Add the project root directory to sys.path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from django.test import TestCase
from utils.firebase import db
from .calculations import *
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RattmWeb.settings')
django.setup()

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
        
        self.transactions = {'0': {'action': 'declined', 'time_completed': '2024-08-31T06:02:27.687Z', 
                                   'longitude': -113.807658, 'merchant_name': '3M Co', 'latitude': -42.372604, 
                                   'customerID': 52, 'amount': 860.27, 'ip_address': '179.152.194.186'}, 
                             '1': {'action': 'declined', 'time_completed': '2023-12-07T08:07:20.451Z', 
                                   'longitude': -1.121183, 'merchant_name': 'Smith Corp', 'latitude': 11.962175, 
                                   'customerID': 74, 'amount': 144.53, 'ip_address': '173.64.65.25'}}
    def test_get_closest_match(self):
        # Test matching "3M Co" to "3M Co" in ESG_scores
        result = get_closest_match("3M", self.esg)
        self.assertEqual(result, "3M Co")
        
        # Test matching "Smith Corp" to "A O Smith Corp"
        result = get_closest_match("Smith Corp", self.esg)
        self.assertEqual(result, "A O Smith Corp")
        
        # Test when there's no match
        result = get_closest_match("Uber", self.esg)
        self.assertEqual(result, None)
        
    def test_get_company_env_score(self):
        transaction = {"merchant_name": "3M Co"}
        result = get_company_env_score(transaction, self.esg)
        self.assertEqual(result, 526)

        transaction = {"merchant_name": "A O Smith Corp"}
        result = get_company_env_score(transaction, self.esg)
        self.assertEqual(result, 510)
        
        # Test matching with "Uber" which should have no match
        transaction = {"merchant_name": "Uber"}
        result = get_company_env_score(transaction, self.esg)
        self.assertEqual(result, 0)
    
    
    def test_get_company_tier(self):
        self.assertEqual(_company_tier(600), 1)
        self.assertEqual(_company_tier(501), 2)
        
    def test_count_green_transactions_in_period(self):
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2024, 1, 1)
        result = _count_green_transactions_in_period(self.transactions, start_date, end_date, self.esg)
        self.assertEqual(result, 1)
        
    def test_get_unique_companies(self):
        result = _get_unique_companies(self.transactions, self.esg)
        self.assertEqual(result, {"3M Co", "A O Smith Corp"})
    
    def test_calculate_score(self):
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2024, 1, 1)
        result = calculate_score(self.transactions, start_date, end_date, self.esg)
        total_spending = 0
        for transaction in self.transactions:
            company_env_score = _get_company_env_score(transaction, self.esg)
            transaction_amount = self.transactions[transaction]['amount']
            env_contribution += company_env_score * transaction_amount
            total_spending += transaction_amount
        expected_result = int(env_contribution / total_spending) if total_spending != 0 else None
        self.assertEqual(result, expected_result)
    
    def test_calculate_company_esg_scores(self):
        result = calculate_company_esg_scores(self.transactions, self.esg)
        expected_result = [{"3M Co": 526}, {"A O Smith Corp": 510}]
        self.assertEqual(result, expected_result)
    
    def test_get_total_green_transactions(self):
        result = get_total_green_transactions(self.transactions, self.esg)
        self.assertEqual(result, 1)
    
    def test_find_most_purchased_companies(self):
        # Expected result: The function should return a list of dictionaries representing the top 5 transactions by amount
        result = find_most_purchased_companies(self.transactions, self.esg)

        # Verify the length of the result (should be up to 5, but in this case only 2 transactions exist)
        self.assertEqual(len(result), 2)

        # Verify the first result is "3M Co" (the highest amount)
        self.assertEqual(result[0]['Company Name'], '3M Co')
        self.assertEqual(result[0]['Amount Spent'], 860.27)
        self.assertEqual(result[0]['ESG Score'], 526)

        # Verify the second result is "Smith Corp" (the next highest amount)
        self.assertEqual(result[1]['Company Name'], 'Smith Corp')
        self.assertEqual(result[1]['Amount Spent'], 144.53)
        self.assertEqual(result[1]['ESG Score'], 0)  # Assuming Smith Corp is not found in ESG scores and defaults to 0

        # Verify the structure of the dictionaries
        for company in result:
            self.assertIn('Company Name', company)
            self.assertIn('ESG Score', company)
            self.assertIn('Amount Spent', company)

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

    def test_is_green(self):
        """Test the _is_green function"""
        # Transaction with company above 500 should be green
        green_transaction = {'merchant_name': '3M Co'}
        self.assertTrue(_is_green(green_transaction, self.esg))

        # Transaction with company exactly at 500 should not be green
        borderline_transaction = {'merchant_name': 'Borderline Company'}
        self.assertFalse(_is_green(borderline_transaction, self.esg))

    def test_company_tier_detailed(self):
        """Test the _company_tier function with more detailed scenarios"""
        self.assertEqual(_company_tier(570), 1, "Score above 560 should be tier 1")
        self.assertEqual(_company_tier(540), 2, "Score between 520 and 560 should be tier 2")
        self.assertEqual(_company_tier(510), 3, "Score between 500 and 520 should be tier 3")
        self.assertEqual(_company_tier(490), 4, "Score below 500 should be tier 4")

    def test_calculate_historical_scores(self):
        """Test the calculate_historical_scores function"""
        # We'll use a subset of transactions to simulate historical data
        historical_scores = calculate_historical_scores(self.transactions, self.esg)
        
        # Verify the length of the returned list
        self.assertEqual(len(historical_scores), 12, "Should return scores for 12 months")
        
        # Verify that the scores are calculated
        self.assertIsNotNone(historical_scores[0], "First month's score should not be None")
        
    def test_calculate_historical_green_transactions(self):
        """Test the calculate_historical_green_transactions function"""
        historical_green_transactions = calculate_historical_green_transactions(self.transactions, self.esg)
        
        # Verify the length of the returned list
        self.assertEqual(len(historical_green_transactions), 12, "Should return green transaction counts for 12 months")
        
        # Verify that the counts are calculated
        self.assertIsNotNone(historical_green_transactions[0], "First month's green transaction count should be calculable")

    def test_find_companies_in_each_tier(self):
        """Test the find_companies_in_each_tier function"""
        tier_counts = find_companies_in_each_tier(self.transactions, self.esg)
        
        # Verify the length of the returned list
        self.assertEqual(len(tier_counts), 4, "Should return counts for 4 tiers")
        
        # Basic assertions about the tier counts
        self.assertGreaterEqual(sum(tier_counts), 0, "Total tier count should be non-negative")
        
        # Specific assertions based on our test data
        # Green Company should be in tier 1
        self.assertGreater(tier_counts[0], 0, "Tier 1 should have at least one company")
        
        # 3M Co should be in tier 3
        tier_3_index = 2
        self.assertIn(tier_counts[tier_3_index], range(4), "Tier count should be a reasonable number")  
        
# if __name__ == '__main__':
#     def get_table_from_firebase(table_to_access: str):
#         try:
#             docs = db.collection(table_to_access).limit(2).stream()
#             ret = {}
#             for doc in docs:
#                 ret[doc.id] = doc.to_dict()
#         except Exception as e:
#             ret = None
#             print(str(e))
#         return ret
#         print(get_table_from_firebase("esg"))
#     print(get_table_from_firebase('esg'))
#     print("================transactions====================\n")
#     print(get_table_from_firebase('transactions'))