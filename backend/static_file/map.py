# get latitude and longitude of transactions of user
from utils.firebase import db
from django.http import JsonResponse

def get_user_all_locations(user_id):
    try:
        user = db.collection('users').document(user_id)

        if not user:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        user_data = user.to_dict()
        user_transactions = user_data["transactions"]
        locations = []
        
        for transaction in user_transactions: 
            curr_location = (transaction['latitude'], transaction['longitude'])
            locations.append(curr_location)

        return locations
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)