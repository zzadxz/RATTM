from utils.firebase import db
from static_file.company_esg_score import company_name_matching, get_company_score
from static_file.env_impact_history import (
    get_score, 
    get_ESG_score_of_transaction_companies, 
    get_total_green_transactions, 
    get_most_purchased_companies, 
    calculate_historical_scores,
    calculate_historical_green_transactions,
    companies_in_each_tier)
from static_file.map import get_all_locations_and_company
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

# IGNORE THIS
"""
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

    weekly_green_transactions = calculate_historical_green_transactions("weekly", current_date, user_transactions, user_id, esg_data)
    monthly_green_transactions = calculate_historical_green_transactions("monthly", current_date, user_transactions, user_id, esg_data)
    
    user_data["environmental_impact_info"]["past_green_transactions"]["weekly"] = weekly_green_transactions
    user_data["environmental_impact_info"]["past_green_transactions"]["monthly"] = monthly_green_transactions

    user_data["top_5_companies"] = get_most_purchased_companies(user_transactions, esg_data)
    user_data["number_companies_in_each_tier"] = []
    user_data["total_green_transactions"] = get_total_green_transactions(user_transactions, esg_data)
    user_data["current_user_score"] = monthly_carbon_scores[0]


    # call functions to get map
    user_data["map_data"] = get_user_all_locations_and_company(user_id)
"""
#-----------------The function broken up into separate URL calls, but then each function will have to call firebase cuz each call will have different requests-----------------#

def get_past_12_month_names() -> list[str]:
    """
    Returns a reordering of ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] based on the current month
    """
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    # Get the current month index (Jan=0, Dec=11)
    current_month_index = datetime.now().month - 1
    
    # Re-arrange the months so it starts from the current month
    reordered_months = months[current_month_index:] + months[:current_month_index]
    
    return reordered_months

def get_weekly_carbon_score(user_id) -> list[int]:
    """
    Returns list of length 12 of carbon scores each week.
    """
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    # reverse the list so that the most recent data point is the last element
    return calculate_historical_scores("weekly", user_transactions, esg_data)[::-1]

def get_monthly_carbon_score(user_id) -> list[int]:
    """
    Returns list of length 12 of carbon scores each month.
    """
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    # reverse the list so that the most recent data point is the last element
    return calculate_historical_scores("monthly", user_transactions, esg_data)[::-1]

def get_weekly_green_transactions(user_id) -> list[int]:
    """
    Returns list of length 12 of # of green transactions each week.
    """
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    return calculate_historical_green_transactions("weekly", user_transactions, esg_data)[::-1]

def get_monthly_green_transactions(user_id) -> list[int]:
    """
    Returns list of length 12 of # of green transactions each month.
    """
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    return calculate_historical_scores("monthly", user_transactions, esg_data)[::-1]
    
def get_total_green_transactions(user_id) -> int:
    """
    Return total number of green transactions ever. 
    """
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    return get_total_green_transactions(user_transactions, esg_data)
    
def get_top_5_companies(user_id) -> dict:
    """
    Returns in dict format:  { 'Company Name' : str, 'ESG Score' : int, 'Amount Spent' : int }
    """
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    return get_most_purchased_companies(user_transactions, esg_data)

def get_total_co2_score(user_id) -> int:
    """
    Returns CO2 score for this month.
    """
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    return calculate_historical_scores("monthly", user_transactions, esg_data)[0]

def get_company_tiers(user_id) -> list[int]:
    """
    Returns list of length 4, where the first index is the number of companies in the highest tier.
    """
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    return companies_in_each_tier(user_transactions, esg_data)

def get_co2_score_change(user_id) -> int:
    """
    Returns the difference between last month and this month's CO2 score.
    """
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    monthly_scores = calculate_historical_scores("monthly", user_transactions, esg_data)
    return monthly_scores[0] - monthly_scores[1]
    
def get_green_transaction_change(user_id) -> int:
    """
    Returns the difference between last month and this month's # of green transactions.
    """
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    monthly_green_transactions = calculate_historical_scores("monthly", user_transactions, esg_data)
    return monthly_green_transactions[0] - monthly_green_transactions[1]
    


# Note that get_map is not needed here beacuse it can be imported from static.get_user_all_locations_and_company

# Added this function here from static_file.map
def get_user_all_locations_and_company(user_id):
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    get_all_locations_and_company(user_transactions, esg_data)