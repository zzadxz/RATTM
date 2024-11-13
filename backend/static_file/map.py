# get latitude and longitude of transactions of user
from utils.firebase import db
from django.http import JsonResponse
from .env_impact_history import _get_closest_match, _company_tier

# def get_user_all_locations(user_id):
#     try:
#         user = db.collection('Users').document(user_id)

#         if not user:
#             return JsonResponse({'error': 'User not found'}, status=404)
        
#         user_data = user.to_dict()
#         user_transactions = user_data["transactions"]
#         locations = []
        
#         for transaction in user_transactions: 
#             curr_location = (transaction['latitude'], transaction['longitude'])
#             locations.append(curr_location)

#         return locations
        
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)
    
    
def get_all_locations_and_company(transactions: dict[int, dict], ESG_scores):
    map_data = []
    
    for transaction in transactions: 
        company_name = _get_closest_match(transaction['merchant_name'], ESG_scores.getkeys())
        transact_map_data = {
            "location": (transaction['latitude'], transaction['longitude']),
            "merchant_name": transaction['merchant_name'],
            "merchant_percentile": _company_tier(ESG_scores[company_name]['environment_score']),
        }
        map_data.append(transact_map_data)

    return map_data