# Assuming that all the transactions in a user is stored in a dict with transaction ID as key
# transactions = {123: {"company": "Apple", "amount": 100, "time":2024-03-06}}
from datetime import datetime

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
        company_env_score = ESG_scores[transaction['merchant_name']]['environment_score']
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
        company_env_score = ESG_scores[transaction['merchant_name']]['environment_score']
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
        company_env_score = ESG_scores[transaction['merchant_name']]['environment_score']
        if company_env_score > 500:
            green_transactions += 1
    
    return green_transactions

def get_most_purchased_companies(transactions: dict[int, dict], ESG_scores: dict[str,dict]) -> list[dict[str, float]]:
    """
    Gets most purchased companies of all time, returns a list of dictionary, where dictionaries 
    contain the company name, the ESG score of the company and the amount spent on that company
    """
    sorted_transactions = sorted(transactions, key=lambda dic: dic['Amount'], reverse=True)
    top_5_companies = []
    for transaction in sorted_transactions[:5]:
        company_env_score = ESG_scores[transaction['merchant_name']]['environment_score']
        top_5_companies.append({
            'Company Name': transaction['merchant_name'],
            'ESG Score': company_env_score,
            'Amount Spent': transaction['amount']
        })
    
    return top_5_companies

def get_user_transactions(all_transactions: dict[int, dict], userID: int):
    """
    Based on a dict containing transactions for all users, return a dict containing 
    only the transactions for the user with the given userID.
    """
    user_transactions = {}
    
    # iterate through all transactions
    for transaction_id in transactions:
        # if the customer ID is this user
        if transactions[transaction_id]["customerID"] == userID:
            # add the transaction to the dict specific to this user
            user_transactions[transaction_id] = transactions[transaction_id]
    return user_transactions

def calculate_scores(frequency: str, current_date: datetime, user_transactions: dict[int, dict], esg_scores: dict[str, dict]):
    scores = []

    if frequency == "weekly":
        delta_days = 7
    elif frequency == "monthly":
        delta_days = 30
    else:
        raise ValueError("Frequency must be 'weekly' or 'monthly'")

    # Loop to calculate scores for the specified frequency
    for _ in range(12):
        start_date = current_date - timedelta(days=delta_days)
        
        # Calculate the score for the current period
        score = get_score(user_transactions, start_date, current_date, esg_scores)
        
        # Append the score
        scores.append(score)
        
        # Move to the previous period
        current_date = start_date
    
    return scores