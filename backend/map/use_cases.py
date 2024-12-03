# get latitude and longitude of transactions of user
from utils.firebase import db
from django.http import JsonResponse
from .calculations import _get_closest_match, _company_tier
from utils.firebase import db
from utils.abstract_data_access import AbstractDataAccess
from .abstract_use_case import AbstractMapUseCase

class MapUseCase(AbstractMapUseCase):
    """
    Implemnted child class of abstract map use case. 
    """
    def __init__(self, data_access: AbstractDataAccess):
        """
        Initialize Map Use Case for the user
        """
        self.data_access = data_access


    def get_user_all_locations_and_company(self, user_id: str):
        """
        Returns a list of transaction details necessary for the map. This use case implement such that 
        company name, location of purchase, and merchant percentile is returned. 
        """
        user_transactions = self.data_access.get_table_from_database('Users')[user_id]['transactions']
        esg_data = self.data_access.get_table_from_database('esg')

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