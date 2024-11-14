from utils.firebase import db
from utils.data_access import get_table_from_firebase
from static_file.company_esg_score import company_name_matching, get_company_score
from static_file.env_impact_history import (
    get_score, 
    get_ESG_score_of_transaction_companies, 
    get_total_green_transactions, 
    get_most_purchased_companies, 
    calculate_historical_scores,
    calculate_historical_green_transactions,
    companies_in_each_tier
    )
from static_file.map import get_all_locations_and_company
from datetime import date

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