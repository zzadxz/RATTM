# get latitude and longitude of transactions of user
from utils.firebase import db
from django.http import JsonResponse
from login.use_cases import get_table_from_firebase
from env_impact_history import get_company_env_score, get_closest_match, company_tier

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
    
    
def get_user_all_locations_and_company(user_id):
    try:
        user = db.collection('Users').document(user_id)

        if not user:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        # This line will just get one user's data from firebase
        User_data = db.collection('Users').document(user_id).get().to_dict()
        user_transactions = User_data["transactions"]
        
        # This line will get all the ESG scores from firebase
        ESG_scores = get_table_from_firebase('esg')
        
        map_data = []
        
        for transaction in user_transactions: 
            company_name = get_closest_match(transaction['merchant_name'], ESG_scores.getkeys())
            transact_map_data = {
                "location": (transaction['latitude'], transaction['longitude']),
                "merchant_name": transaction['merchant_name'],
                "merchant_percentile": company_tier(ESG_scores[company_name]['environment_score']),
            }
            map_data.append(transact_map_data)

        return map_data
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)