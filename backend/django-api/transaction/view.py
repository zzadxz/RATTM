from django.shortcuts import render

from django.http import JsonResponse
from RattmWeb.firebase import db

# Put data in Firestore
def upload_data_to_firestore(request):
    data = {
        "Transaction ID": "TXN001",
        "Client ID": "CL001",
        "Date": "2024-09-01",
        "Company Name": "EcoMarket",
        "Location - Latitude": 40.7128,
        "Location - Longitude": -74.006,
        "Transaction Amount": 45.5
    }

    try:
        # don't need to first create the table, can just start adding and the table will be created
        db.collection('transactions').add(data) 
        return JsonResponse({'message': 'Data uploaded successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Get data from Firestore
def get_data_from_firestore(request):
    try:
        transactions_ref = db.collection('transactions')
        docs = transactions_ref.stream()

        transactions = []
        # a document is a row in the table (transaction obj)
        for doc in docs:
            transaction = doc.to_dict()
            transaction["rating"] = esg_rating(transaction)
            transactions.append(transaction)

        return JsonResponse(transactions, safe=False, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

# Fake function rn to give esg rating for company
def esg_rating(transaction_dict):
    return len(transaction_dict["Company Name"]) // 3