# import sys
# import os

# # Add the project root directory to sys.path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from django.test import TestCase
from utils.firebase import db
from .calculations import *

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