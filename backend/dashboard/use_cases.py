from utils.firebase import db
from utils.data_access import get_table_from_firebase
from .calculations import (
    calculate_score, 
    calculate_company_esg_scores, 
    calculate_total_green_transactions, 
    find_most_purchased_companies, 
    calculate_historical_scores,
    calculate_historical_green_transactions,
    find_companies_in_each_tier
)
from datetime import date

def past_12_month_names() -> list[str]:
    """
    Returns a reordering of ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] based on the current month
    """
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    # Get the current month index (Jan=0, Dec=11)
    current_month_index = datetime.now().month - 1
    
    # Re-arrange the months so it starts from the current month
    reordered_months = months[current_month_index:] + months[:current_month_index]
    
    return reordered_months

def weekly_carbon_scores(user_id) -> list[int]:
    """
    Returns list of length 12 of carbon scores each week.
    """
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    # reverse the list so that the most recent data point is the last element
    return calculate_historical_scores("weekly", user_transactions, esg_data)[::-1]

def monthly_carbon_scores(user_id) -> list[int]:
    """
    Returns list of length 12 of carbon scores each month.
    """
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    # reverse the list so that the most recent data point is the last element
    return calculate_historical_scores("monthly", user_transactions, esg_data)[::-1]

def weekly_green_transactions(user_id) -> list[int]:
    """
    Returns list of length 12 of # of green transactions each week.
    """
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    return calculate_historical_green_transactions("weekly", user_transactions, esg_data)[::-1]

def monthly_green_transactions(user_id) -> list[int]:
    """
    Returns list of length 12 of # of green transactions each month.
    """
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    return calculate_historical_scores("monthly", user_transactions, esg_data)[::-1]
    
def total_green_transactions(user_id) -> int:
    """
    Return total number of green transactions ever. 
    """
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    return calculate_total_green_transactions(user_transactions, esg_data)
    
def top_5_companies(user_id) -> dict:
    """
    Returns in dict format:  { 'Company Name' : str, 'ESG Score' : int, 'Amount Spent' : int }
    """
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    return find_most_purchased_companies(user_transactions, esg_data)

def total_co2_score(user_id) -> int:
    """
    Returns CO2 score for this month.
    """
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    return calculate_historical_scores("monthly", user_transactions, esg_data)[0]

def company_tiers(user_id) -> list[int]:
    """
    Returns list of length 4, where the first index is the number of companies in the highest tier.
    """
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    return find_companies_in_each_tier(user_transactions, esg_data)

def co2_score_change(user_id) -> int:
    """
    Returns the difference between last month and this month's CO2 score.
    """
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    monthly_scores = calculate_historical_scores("monthly", user_transactions, esg_data)
    return monthly_scores[0] - monthly_scores[1]
    
def green_transaction_change(user_id) -> int:
    """
    Returns the difference between last month and this month's # of green transactions.
    """
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    monthly_green_transactions = calculate_historical_scores("monthly", user_transactions, esg_data)
    return monthly_green_transactions[0] - monthly_green_transactions[1]
    