from utils.firebase import db
from static_file.company_esg_score import company_name_matching, get_company_score
from static_file.env_impact_history import get_score, get_ESG_score_of_transaction_companies, get_total_green_transactions, get_most_purchased_companies, get_user_transactions, calculate_historical_scores
from static_file.map import get_user_all_locations_and_company
from datetime import date

def get_table_from_firebase(table_to_access: str):
    """
    Return a dict mapping the key of the firestore collection to the data within its rows.
    """
    try:
        docs = db.collection(table_to_access).stream()
        ret = {}
        for doc in docs:
            ret[doc.id] = doc.to_dict()
    except Exception as e:
        ret = None
        print(str(e))
    return ret

def return_user_data(request)-> dict[dict]:
    # Retrieve cached user_id from session
    user_id = request.session.get("user_id")
    if user_id is None:
        return {"error": "User ID not found in session"}

    # Pull from 
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']

    # ESG DATA
    esg_data = get_table_from_firebase('esg')

    user_data = {
        "map_data": {}, # { merchant_name : { "latitude" : latitude, "longitude" : longitude, "esg_score" : company_esg_score, "amount_spent" : amount_spent } }
        "environmental_impact_info": {
            "past_green_transactions" : {
                "weekly":[], 
                "monthly":[] # list of length 12
            }, 
            "past_carbon_scores" : {
                "weekly":[], 
                "monthly":[] # list of length 12
            }, 
            "top_5_companies" : {}, # { 'Company Name' : '', 'ESG Score' : 0, 'Amount Spent' : 0 }
            "number_companies_in_each_tier" : [], # list of length 4
            "current_user_score" : 0,
            "total_green_transactions" : 0
        }
    }
    
    current_date = date.today()

    weekly_carbon_scores = calculate_historical_scores("weekly", current_date, user_transactions, user_id, esg_data)
    monthly_carbon_scores = calculate_historical_scores("monthly", current_date, user_transactions, user_id, esg_data)

    user_data["environmental_impact_info"]["past_carbon_scores"]["weekly"] = weekly_carbon_scores
    user_data["environmental_impact_info"]["past_carbon_scores"]["monthly"] = monthly_carbon_scores

    user_data["environmental_impact_info"]["past_green_transactions"]["weekly"] = None
    user_data["environmental_impact_info"]["past_green_transactions"]["monthly"] = None

    user_data["top_5_companies"] = get_most_purchased_companies(user_transactions, esg_data)
    user_data["number_companies_in_each_tier"] = []
    user_data["total_green_transactions"] = get_total_green_transactions(user_transactions, esg_data)
    user_data["current_user_score"] = monthly_carbon_scores[0]


    # call functions to get map
    user_data["map_data"] = get_user_all_locations_and_company(user_id)
    
#-----------------The function broken up into separate URL calls, but then each function will have to call firebase cuz each call will have different requests-----------------#

def get_weekly_carbon_score(request):
    try:
        current_date = date.today()
        user_id = request.session.get("user_id")
        # Pull from firebase
        User_data = db.collection('Users').document(user_id).get().to_dict()
        user_transactions = User_data["transactions"]
        
        if not User_data:
            return {"error": "User ID not found in session"}
        # ESG DATA
        esg_data = get_table_from_firebase('esg')
        
        # Unique to this function
        weekly_carbon_scores = calculate_historical_scores("weekly", current_date, user_transactions, user_id, esg_data)
        
        return weekly_carbon_scores
    except Exception as e:
        return {"error": str(e)}
    

def get_monthly_carbon_score(request):
    try:
        current_date = date.today()
        user_id = request.session.get("user_id")
        # Pull from firebase
        User_data = db.collection('Users').document(user_id).get().to_dict()
        user_transactions = User_data["transactions"]
        
        if not User_data:
            return {"error": "User ID not found in session"}
        # ESG DATA
        esg_data = get_table_from_firebase('esg')
        
        # Unique to this function
        monthly_carbon_scores = calculate_historical_scores("monthly", current_date, user_transactions, user_id, esg_data)
        
        return monthly_carbon_scores
    except Exception as e:
        return {"error": str(e)}

def get_weekly_green_transactions(request):
    return NotImplementedError

def get_monthly_green_transactions(request):
    return NotImplementedError
    
def get_total_green_transactions(request):
    try:
        current_date = date.today()
        user_id = request.session.get("user_id")
        # Pull from firebase
        User_data = db.collection('Users').document(user_id).get().to_dict()
        user_transactions = User_data["transactions"]
        
        if not User_data:
            return {"error": "User ID not found in session"}
        # ESG DATA
        esg_data = get_table_from_firebase('esg')
        
        # Unique to this function
        total_green_transactions = get_total_green_transactions(user_transactions, esg_data)
        
        return total_green_transactions
    except Exception as e:
        return {"error": str(e)}
    
def get_top_companies(request):
    try:
        current_date = date.today()
        user_id = request.session.get("user_id")
        # Pull from firebase
        User_data = db.collection('Users').document(user_id).get().to_dict()
        user_transactions = User_data["transactions"]
        
        if not User_data:
            return {"error": "User ID not found in session"}
        # ESG DATA
        esg_data = get_table_from_firebase('esg')
        
        # Unique to this function
        top_companies = get_most_purchased_companies(user_transactions, esg_data)
        
        return top_companies
    except Exception as e:
        return {"error": str(e)}

def get_total_co2_score(request):
    return NotImplementedError

def get_company_tiers(request):
    return NotImplementedError

def get_co2_score_change(request):
    return NotImplementedError
    
def get_green_transaction_change(request):
    return NotImplementedError
    



# Note that get_map is not needed here beacuse it can be imported from static.get_user_all_locations_and_company