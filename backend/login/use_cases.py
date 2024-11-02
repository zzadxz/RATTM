from utils.firebase import db

def get_table_from_firebase(table_to_access):
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

def get_user_transactions(all_transactions, userID):
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

def return_user_data(request):
    # Retrieve cached user_id from session
    user_id = request.session.get("user_id")
    if user_id is None:
        return {"error": "User ID not found in session"}

    # TRANSACTIONS SPECIFIC TO THIS USER
    all_transactions = get_table_from_firebase('transactions')
    user_transactions = get_user_transactions(all_transactions, user_id)

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
            "top_10_companies" : {}, # { merchant_name : (esg_score, total_amount_purchased) }
            "number_companies_in_each_tier" : [], # list of length 4
            "current_user_score" : 0,
        }
    }

    # call functions to get env impact info

    # call functions to get map