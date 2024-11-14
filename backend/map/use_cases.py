# get latitude and longitude of transactions of user
from utils.firebase import db
from django.http import JsonResponse
from .env_impact_history import _get_closest_match, _company_tier
from utils.firebase import db
from utils.data_access import get_table_from_firebase

# Note that get_map is not needed here beacuse it can be imported from static.get_user_all_locations_and_company

# Added this function here from static_file.map
def get_user_all_locations_and_company(user_id):
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')

    print(esg_data, user_transactions)

    map_data = []
    
    for transaction in user_transactions: 
        company_name = _get_closest_match(transaction['merchant_name'], esg_data.getkeys())
        transact_map_data = {
            "location": (transaction['latitude'], transaction['longitude']),
            "merchant_name": transaction['merchant_name'],
            "merchant_percentile": _company_tier(esg_data[company_name]['environment_score']),
        }
        map_data.append(transact_map_data)

    return map_data

get_user_all_locations_and_company(1)