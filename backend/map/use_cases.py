# get latitude and longitude of transactions of user
from utils.firebase import db
from django.http import JsonResponse
from .calculations import _get_closest_match, _company_tier
from utils.firebase import db
from utils.data_access import get_table_from_firebase
from .abstract_use_case import AbstractMapUseCase

class MapUseCase(AbstractMapUseCase):
    """
    Implemnted child class of abstract map use case. 
    """
    def __init__(self, user_id):
        """
        Initialize Map Use Case for the user"""
        self.user_id = user_id


    def get_user_all_locations_and_company(self):
        """
        Returns a list of transaction details necessary for the map. This use case implement such that 
        company name, location of purchase, and merchant percentile is returned. 
        """
        user_transactions = get_table_from_firebase('Users')[self.user_id]['transactions']
        esg_data = get_table_from_firebase('esg')

        map_data = []
        
        for transaction in user_transactions: 
            company_name = _get_closest_match(transaction['merchant_name'], list(esg_data.keys()))

            if company_name: 
                transact_map_data = {
                    "location": (transaction['latitude'], transaction['longitude']),
                    "merchant_name": transaction['merchant_name'],
                    "merchant_percentile": _company_tier(esg_data[company_name]['environment_score']),
                }
                map_data.append(transact_map_data)
            else: 
                transact_map_data = {
                    "location": (transaction['latitude'], transaction['longitude']),
                    "merchant_name": transaction['merchant_name'],
                    "merchant_percentile": "No environmental score available for " + transaction['merchant_name'] + ". ",
                }

        return map_data