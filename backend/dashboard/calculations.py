from datetime import datetime, timedelta
from calendar import monthrange
from rapidfuzz import process
from dateutil.relativedelta import relativedelta

def _get_closest_match(query: str, choices: dict, score_cutoff: int = 75) -> str:
    """
    Returns the best match for query in the keys of choices dict if the score 
    is above the score_cutoff.
    """
    match, score, _ = process.extractOne(query, choices.keys())
    if score >= score_cutoff:
        return match
    return None

def _get_company_env_score(transaction: dict, ESG_scores: dict[str, dict]):
    """
    Returns environmental score for a transaction's company IF the company is in the ESG_scores dict.
    Otherwise, return 0.
    """
    company_name = _get_closest_match(transaction['merchant_name'], ESG_scores)
    if company_name is not None:
        return ESG_scores[company_name]['environment_score']
    else:
        return 0

def _is_green(transaction: dict, ESG_scores: dict[str,dict]):
    company_env_score = _get_company_env_score(transaction, ESG_scores)
    return company_env_score > 500

def _company_tier(company_env_score: int) -> int:
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
    

def _get_start_end_dates(current_date: datetime) -> tuple[datetime]:
    """
    Helper function, get start and end dates of the month of the current_date.
    """
    # Get the first day of the month
    start_date = current_date.replace(day=1)
    # Get the last day of the month
    last_day = monthrange(current_date.year, current_date.month)[1]
    end_date = current_date.replace(day=last_day)
    
    return start_date, end_date



def _count_green_transactions_in_period(transactions: list[dict], start_date: datetime, end_date: datetime, ESG_scores: dict[str,dict]) -> int:
    """
    Helper function that counts green transactions within a specified date range.
    """
    return sum(
        1 for transaction in transactions
        if start_date <= datetime.strptime(transaction['time_completed'], "%Y-%m-%dT%H:%M:%S.%fZ") <= end_date
        and _is_green(transaction, ESG_scores)
    )


def _get_unique_companies(transactions: list[dict], ESG_scores: dict[str, dict]):
    """
    Return set of unique companies in transaction
    """
    unique_companies = set()

    for transaction in transactions:
        company_name = _get_closest_match(transaction['merchant_name'], ESG_scores)
        if company_name:
            unique_companies.add(company_name)
    return unique_companies


def calculate_score(transactions: list[dict], start: datetime, end: datetime, ESG_scores: dict[str, dict]) -> float:
    """
    Calculate the environmental impact score of a user
    """
    lst_of_transactions = []
    for transaction in transactions:
        transaction_date = datetime.strptime(transaction['time_completed'], "%Y-%m-%dT%H:%M:%S.%fZ")
        if start <= transaction_date <= end:
            lst_of_transactions.append(transaction)

    # Env_Contribution
    env_contribution = 0
    total_spending = 0
    for transaction in lst_of_transactions:
        company_env_score = _get_company_env_score(transaction, ESG_scores)
        transaction_amount = transaction['amount']
        env_contribution += company_env_score * transaction_amount
        total_spending += transaction_amount
    
    return int(env_contribution / total_spending) if total_spending != 0 else None


def calculate_company_esg_scores(transactions: dict[int, dict], ESG_scores: dict[str,dict]) -> list[dict[str, float]]:
    """
    Calculate the ESG score of the companies that the user has made transactions with
    """
    company_ESG_scores = []
    for transaction in transactions:
        company_env_score = _get_company_env_score(transaction, ESG_scores)
        company_ESG_scores.append({transaction['merchant_name']: company_env_score})
    
    return company_ESG_scores


def calculate_total_green_transactions(transactions: list[dict], ESG_scores: dict[str,dict]) -> int:
    """
    25th percentile: 245.0
    50th percentile: 500.0
    75th percentile: 520.0
    90th percentile: 560.0
    """
    green_transactions = 0
    for transaction in transactions:
        if _is_green(transaction, ESG_scores):
            green_transactions += 1
    
    return green_transactions


def find_most_purchased_companies(transactions: dict[int, dict], ESG_scores: dict[str,dict]) -> list[dict[str, float]]:
    """
    Gets most purchased companies of all time, returns a list of dictionary, where dictionaries 
    contain the company name, the ESG score of the company and the amount spent on that company
    """
    sorted_transactions = sorted(transactions, key=lambda dic: dic['amount'], reverse=True)
    top_5_companies = []
    for transaction in sorted_transactions[:5]:
        company_env_score = _get_company_env_score(transaction, ESG_scores)
        top_5_companies.append({
            'Company Name': transaction['merchant_name'],
            'ESG Score': company_env_score,
            'Amount Spent': transaction['amount']
        })
    
    return top_5_companies


def calculate_historical_scores(transactions: dict[int, dict], esg_scores: dict[str, dict]) -> list[int]:
    """
    Return list of environmental scores for the past 12 months.
    The scores go from most to least recent! So scores[0] is this month, scores[-1] is 10 months ago
    """
    scores = []
    current_date =  datetime.now() - relativedelta(months=1)
    delta_days = 30

    for _ in range(12):
        # Get start and end dates
        start_date, end_date = _get_start_end_dates(current_date)
        
        # Calculate the score for the current period
        score = calculate_score(transactions, start_date, end_date, esg_scores)
        
        scores.append(score)
        
        current_date = start_date - timedelta(days=start_date.day)

    return scores


def calculate_historical_green_transactions(transactions: dict[int, dict], ESG_scores: dict[str,dict]) -> list[int]:
    """
    Return a list of green transaction counts for the past months.
    List goes from most recent as first element to least recent as last element.
    """
    green_transaction_counts = []
    current_date =  datetime.now() - relativedelta(months=1)

    for _ in range(12):
        # Get start and end dates for this period
        start_date, end_date = _get_start_end_dates(current_date)
        
        # Get the number of green transactions for the current period
        green_count = _count_green_transactions_in_period(transactions, start_date, end_date, ESG_scores)
        
        green_transaction_counts.append(green_count)
        
        current_date = start_date - timedelta(days=start_date.day)

    return green_transaction_counts


def find_companies_in_each_tier(transactions: list[dict], ESG_scores: dict[str, dict]) -> list[int]:
    """
    Returns list of length 4, where the first element is the number of companies in the highest tier
    that the user shopped at for all time.
    """
    # Set of unique companies transacted with this month
    unique_companies_this_month = _get_unique_companies(transactions, ESG_scores)

    # Indices correspond to tiers 1-4
    company_tier_counts = [0, 0, 0, 0]  

    # Classify each unique company into a tier and count
    for company_name in unique_companies_this_month:
        company_env_score = ESG_scores[company_name]['environment_score']
        tier_index = _company_tier(company_env_score) - 1 
        company_tier_counts[tier_index] += 1

    return company_tier_counts