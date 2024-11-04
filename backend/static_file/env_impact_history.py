from datetime import datetime, timedelta
from calendar import monthrange
from rapidfuzz import process

def get_closest_match(query: str, choices: dict, score_cutoff: int = 75) -> str:
    """
    Returns the best match for query in the keys of choices dict if the score 
    is above the score_cutoff.
    """
    match, score = process.extractOne(query, choices.keys())
    if score >= score_cutoff:
        return match
    return None

def get_company_env_score(transaction: dict, ESG_scores: dict[str, dict]):
    """
    Returns environmental score for a transaction's company IF the company is in the ESG_scores dict.
    Otherwise, return 0.
    """
    company_name = get_closest_match(transaction['merchant_name'], ESG_scores)
    if company_name is not None:
        return ESG_scores[company_name]['environment_score']
    else:
        return 0

# Assuming that the ESG_scores is a dictionary, 
# whose key is the company's name and the value is the ESG score of the company
def get_score(transactions: dict[int, dict], start: datetime, end: datetime, ESG_scores: dict[str, dict]) -> float:
    """
    Calculate the environmental impact score of a user
    """
    # Assuming that we are able to get the transaction history of the user from
    # start date to end date as a list, and we have figured out how to parse through the
    # the company names, so each entry is a dictionary with the company name as the key
    # and the transaction amount as the value
    lst_of_transactions = []
    for transaction in transactions.values():
        transaction_date = datetime.strptime(transaction['time_completed'], "%Y-%m-%dT%H:%M:%S.%fZ")
        if start <= transaction_date <= end:
            lst_of_transactions.append(transaction)

    # Env_Contribution
    env_contribution = 0
    total_spending = 0
    for transaction in lst_of_transactions:
        company_env_score = get_company_env_score(transaction, ESG_scores)
        transaction_amount = transaction['amount']
        env_contribution += company_env_score * transaction_amount
        total_spending += transaction_amount
    
    return env_contribution / total_spending

def get_ESG_score_of_transaction_companies(transactions: dict[int, dict], ESG_scores: dict[str,dict]) -> list[dict[str, float]]:
    """
    Calculate the ESG score of the companies that the user has made transactions with
    """
    company_ESG_scores = []
    for transaction in transactions:
        company_env_score = get_company_env_score(transaction, ESG_scores)
        company_ESG_scores.append({transaction['merchant_name']: company_env_score})
    
    return company_ESG_scores

def get_total_green_transactions(transactions: dict[int, dict], ESG_scores: dict[str,dict]) -> int:
    """
    25th percentile: 245.0
    50th percentile: 500.0
    75th percentile: 520.0
    90th percentile: 560.0
    """
    green_transactions = 0
    for transaction in transactions:
        company_env_score = get_company_env_score(transaction, ESG_scores)
        if company_env_score > 500:
            green_transactions += 1
    
    return green_transactions

def company_tier(company_env_score: int) -> int:
    """
    Returns the tier of the company based on its environmental score, 
    worst tier is 4 and best tier is 1.
    """
    if company_env_score > 560:
        return 1
    elif company_env_score > 520:
        return 2
    elif company_env_score > 500:
        return 3
    else:
        return 4
    

def get_most_purchased_companies(transactions: dict[int, dict], ESG_scores: dict[str,dict]) -> list[dict[str, float]]:
    """
    Gets most purchased companies of all time, returns a list of dictionary, where dictionaries 
    contain the company name, the ESG score of the company and the amount spent on that company
    """
    sorted_transactions = sorted(transactions, key=lambda dic: dic['amount'], reverse=True)
    top_5_companies = []
    for transaction in sorted_transactions[:5]:
        company_env_score = get_company_env_score(transaction, ESG_scores)
        top_5_companies.append({
            'Company Name': transaction['merchant_name'],
            'ESG Score': company_env_score,
            'Amount Spent': transaction['amount']
        })
    
    return top_5_companies


# THIS CAN BE REMOVED
def get_user_transactions(all_transactions: dict[int, dict], userID: int):
    """
    Based on a dict containing transactions for all users, return a dict containing 
    only the transactions for the user with the given userID.
    """
    user_transactions = {}
    
    # iterate through all transactions
    for transaction_id in all_transactions:
        # if the customer ID is this user
        if all_transactions[transaction_id]["customerID"] == userID:
            # add the transaction to the dict specific to this user
            user_transactions[transaction_id] = all_transactions[transaction_id]
    return user_transactions

def _get_start_end_dates(frequency: str, current_date: datetime) -> tuple[datetime]:
    """
    Helper function, get start and end dates of the week or month of the current_date.
    """
    if frequency == "weekly":
        # Get the start of the week (Monday)
        start_date = current_date - timedelta(days=current_date.weekday())
        # Get the end of the week (Sunday)
        end_date = start_date + timedelta(days=6)
    elif frequency == "monthly":
        # Get the first day of the month
        start_date = current_date.replace(day=1)
        # Get the last day of the month
        last_day = monthrange(current_date.year, current_date.month)[1]
        end_date = current_date.replace(day=last_day)
    else:
        raise ValueError("Frequency must be 'weekly' or 'monthly'")
    
    return start_date, end_date

def calculate_historical_scores(frequency: str, current_date: datetime, user_transactions: dict[int, dict], esg_scores: dict[str, dict]) -> list[int]:
    """
    Return list of environmental scores for the past 12 weeks or months.
    """
    scores = []

    if frequency == "weekly":
        delta_days = 7
    elif frequency == "monthly":
        delta_days = 30
    else:
        raise ValueError("Frequency must be 'weekly' or 'monthly'")

    for _ in range(12):
        # Get start and end dates based on frequency
        start_date, end_date = _get_start_end_dates(frequency, current_date)
        
        # Calculate the score for the current period
        score = get_score(user_transactions, start_date, end_date, esg_scores)
        
        scores.append(score)
        
        # Increment current date
        if frequency == "weekly":
            current_date = start_date - timedelta(days=1)
        elif frequency == "monthly":
            current_date = start_date - timedelta(days=start_date.day)

    return scores
