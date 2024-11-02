from django.shortcuts import render
from utils.firebase import db
from django.http import JsonResponse

# create 

def get_all_transactions(user_id):
    # Get all transactions from Firestore
    try:
        transactions_ref = db.collection('transactions')
        docs = transactions_ref.stream()

        transactions = []
        # a document is a row in the table (transaction obj)
        for doc in docs:
            transaction = doc.to_dict()
            if transaction["customerID"] == user_id:
                transactions.append(transaction)

        return transactions
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def 