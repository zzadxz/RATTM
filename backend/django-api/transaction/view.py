from django.shortcuts import render

from django.http import JsonResponse
from RattmWeb.firebase import db
from dotenv import load_dotenv
import csv
import json
import os

def make_json(csvFilePath, jsonFilePath):
    # create a dictionary
    data = {}
    
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        
        # Convert each row into a dictionary 
        # and add it to data
        for rows in csvReader:
            
            # Assuming a column named 'No' to
            # be the primary key
            key = rows['No']
            data[key] = rows

    # Open a json writer, and use the json.dumps() 
    # function to dump data
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

# Put data in Firestore
def upload_data_to_firestore(request):
    load_dotenv()
    mock_json_path = os.getenv('MOCK_JSON_PATH')
    with open(mock_json_path, 'r') as file:
        data = json.load(file)

    try:
        # don't need to first create the table, can just start adding and the table will be created
        # data is a dictionary with {key - transactionid : value - {dict of all transaction info}}
        for transaction_id in data:
            db.collection('transactions').add(data[transaction_id])
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
    print(transaction_dict)
    return len(transaction_dict["Company Name"]) // 3