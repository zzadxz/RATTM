# Assuming that all the transactions in a user is stored in a list of dictionaries
# transactions = [{"company": "Apple", "amount": 100, "time":2024-03-06}]
from datetime import datetime

# Assuming that the ESG_scores is a dictionary, 
# whose key is the company's name and the value is the ESG score of the company
def get_score(user: ..., start: datetime, end: datetime, ESG_scores: dict) -> float:
    """
    Calculate the environmental impact score of a user
    """
    # Assuming that we are able to get the transaction history of the user from
    # start date to end date as a list, and we have figured out how to parse through the
    # the company names, so each entry is a dictionary with the company name as the key
    # and the transaction amount as the value
    lst_of_transactions = [
        transaction for transaction in user.transactions
        if start <= transaction['time'] <= end
    ]
    # Env_Contribution
    env_contribution = 0
    total_spending = 0
    for transaction in lst_of_transactions:
        company_env_score = ESG_scores[transaction['Company Name']]
        transaction_amount = transaction['Amount']
        env_contribution += company_env_score * transaction_amount
        total_spending += transaction_amount
    
    return env_contribution / total_spending

def get_ESG_score_of_transaction_companies(user: ..., ESG_scores: dict) -> list[dict[str, float]]:
    """
    Calculate the ESG score of the companies that the user has made transactions with
    """
    lst_of_transactions = user.transactions
    company_ESG_scores = []
    for transaction in lst_of_transactions:
        company_env_score = ESG_scores[transaction['Company Name']]
        company_ESG_scores.append({transaction['Company Name']: company_env_score})
    
    return company_ESG_scores

def get_total_green_transactions(user: ..., ESG_scores: dict) -> int:
    """
    25th percentile: 245.0
    50th percentile: 500.0
    75th percentile: 520.0
    90th percentile: 560.0
    """
    lst_of_transactions = user.transactions
    green_transactions = 0
    for transaction in lst_of_transactions:
        company_env_score = ESG_scores[transaction['Company Name']]
        if company_env_score > 500:
            green_transactions += 1
    
    return green_transactions

def get_most_purchased_companies(user: ..., ESG_scores: dict) -> list[dict[str, float]]:
    """
    Gets most purchased companies of all time, returns a list of dictionary, where dictionaries 
    contain the company name, the ESG score of the company and the amount spent on that company
    """
    sorted_transactions = sorted(user.transactions, key=lambda dic: dic['Amount'], reverse=True)
    top_5_companies = []
    for transaction in sorted_transactions[:5]:
        company_env_score = ESG_scores[transaction['Company Name']]
        top_5_companies.append({
            'Company Name': transaction['Company Name'],
            'ESG Score': company_env_score,
            'Amount Spent': transaction['Amount']
        })
    
    return top_5_companies

    
