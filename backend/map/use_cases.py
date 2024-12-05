# get latitude and longitude of transactions of user
from utils.firebase import db
from django.http import JsonResponse
from .calculations import _get_closest_match, _company_tier
from utils.firebase import db
from utils.abstract_data_access import AbstractDataAccess
from .abstract_use_case import AbstractMapUseCase
import random

class MapUseCase(AbstractMapUseCase):
    """
    Implemnted child class of abstract map use case. 
    """
    def __init__(self, data_access: AbstractDataAccess):
        """
        Initialize Map Use Case for the user
        """
        self.data_access = data_access

    def _convert_to_valid_us_location(self, lat, lon):
        """
        Adjusts the given latitude and longitude to a valid point located on U.S. land.
        """
        # Approximate boundaries for the contiguous United States
        min_lat, max_lat = 32.396308, 37.384358  # Latitude range
        min_lon, max_lon = -105.848974, -85.885444  # Longitude range

        # Check if the point is within the U.S. boundaries
        if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
            return lat, lon
        else:
            # Generate a random point within the U.S. boundaries
            new_lat = random.uniform(min_lat, max_lat)
            new_lon = random.uniform(min_lon, max_lon)
            return new_lat, new_lon


    def get_user_all_locations_and_company(self, user_id: str):
        """
        Returns a list of transaction details necessary for the map. This use case implements such that 
        company name, location of purchase, and merchant percentile is returned.
        """
        user_transactions = self.data_access.get_table_from_database('users')[user_id]['transactions']
        esg_data = self.data_access.get_table_from_database('esg')

        map_data = []

        for transaction in user_transactions:
            company_name = _get_closest_match(transaction['merchant_name'], list(esg_data.keys()))

            # Convert to valid U.S. location
            valid_lat, valid_lon = self._convert_to_valid_us_location(transaction['latitude'], transaction['longitude'])

            if company_name:
                transact_map_data = {
                    "location": (valid_lat, valid_lon),
                    "merchant_name": transaction['merchant_name'],
                    "merchant_percentile": _company_tier(esg_data[company_name]['environment_score']),
                }
                map_data.append(transact_map_data)
            else:
                transact_map_data = {
                    "location": (valid_lat, valid_lon),
                    "merchant_name": transaction['merchant_name'],
                    "merchant_percentile": f"No environmental score available for {transaction['merchant_name']}.",
                }
                map_data.append(transact_map_data)  # Don't forget to append in the else block

        return map_data