from django.shortcuts import render
from utils.firebase import db
from django.http import JsonResponse

def get_all_transactions():
    # Get all transactions from Firestore
    # return a mapping of user_id to a list of all transactions associated with that user
    # can be changed to just transaction id, but then we need to access the transaction collection again

    try:
        transactions_ref = db.collection('transactions')
        all_transactions = transactions_ref.stream()

        user_to_transaction = {i : [] for i in range(100)}
        for transaction in all_transactions:
            user_to_transaction[transaction.to_dict()['customerID']].append(transaction)

        return user_to_transaction
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
