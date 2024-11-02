from django.shortcuts import render
from django.http import JsonResponse
from esg.views import get_data_from_firestore
from utils.firebase import db
from dotenv import load_dotenv
import csv
import json
import os

"""
The end result is a dictionary of users:
{user1:..., user2:..., user3:...}, where each userid is the key and the fields of the users are the value.
take user1 for example, it will map to a dictionary of fields:
users["1"] = {
        "transactions": [] # list of transactions, each transaction is a dictionary
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
"""

def collection_to_list(collection_reference) -> list[dict]:
    """Fetches all documents from a specific Firestore collection and returns
    them as a list of dictionaries.
    
    Args:
        collection_reference example: db.collection('esg')
    """
    documents = collection_reference.stream()
    data_list = []
    
    for doc in documents:
        doc_data = doc.to_dict()  # Convert each document to a dictionary
        doc_data['id'] = doc.id   # Here, the document id is actually the comapny name
        data_list.append(doc_data)
    
    return data_list

# This function is for testing purposes
def collection_to_list_limited(collection_reference, limit=2):
    # Use .limit() to fetch only a specified number of documents
    documents = collection_reference.limit(limit).stream()
    data_list = []
    
    for doc in documents:
        doc_data = doc.to_dict()  # Convert each document to a dictionary
        doc_data['id'] = doc.id   # Optionally include the document ID if needed
        data_list.append(doc_data)
    
    return data_list
    
def esg_data_normalization(collection_data: list[dict]):
    # Normalizing the score to be between 0 and 1
    environment_scores = []
    
    # First file read to get the min and max scores
    for row in collection_data:
        environment_score = float(row['environment_score'])
        environment_scores.append(environment_score)
    min_score = min(environment_scores)
    max_score = max(environment_scores)
    
    normalized_data = []
    for row in collection_data:
        company_name = row['id']
        environment_score = float(row['environment_score'])
        environment_grade = row['environment_grade']
        normalized_score = (environment_score - min_score) / (max_score - min_score)
        data = {
            'company_name': company_name,
            'environment_grade': environment_grade,
            'environment_score': environment_score,
            'normalized_score': normalized_score
        }
        normalized_data.append(data)
    return normalized_data

def populate_user_transactions(tranaction_data: list[dict], User_data: dict) -> None:
    for transaction in tranaction_data:
        if transaction['customerID'] not in User_data:
            User_data[transaction['customerID']] = {}
            User_data[transaction['customerID']]['transactions'] = [transaction]
        else:
            User_data[transaction['customerID']]['transactions'].append(transaction)


def upload_user_data(User_data: dict) -> None:
    if User_data:
        # Testing for connection to firebase
        try: 
            doc = db.collection('test').document('testDoc')
            doc.set({'connected': True})
            print("Firebase is connected, and data was written successfully.")
        except Exception as e:
            print("Connection Error:", e)
        # Now we're uploading the User data
        try:
            for user_id in User_data:
                print(User_data[user_id])
                db.collection('Users').document(str(user_id)).set(User_data[user_id])
            print("User data uploaded successfully.")
        except Exception as e:
            print("Error:", e)
        
if __name__ == '__main__':
    esg_collection = db.collection('esg')
    esg_data = collection_to_list_limited(esg_collection, limit=3)
    print("\nRaw esg_data:\n")
    print(esg_data)
    #[{'environment_level': 'High', 'social_grade': 'BB', 'governance_level': 'Medium', 'social_level': 'Medium', 'total_score': 1141, 'total_grade': 'BBB', 'social_score': 310, 'weburl': 'https://www.3m.com/', 'exchange': 'NEW YORK STOCK EXCHANGE, INC.', 'cik': 66740, 'logo': 'https://static.finnhub.io/logo/2a1802fa-80ec-11ea-a0f5-00000000092a.png', 'industry': 'Industrial Conglomerates', 'governance_score': 305, 'total_level': 'High', 'currency': 'USD', 'governance_grade': 'BB', 'environment_score': 526, 'last_processing_date': '16-04-2022', 'environment_grade': 'A', 'ticker': 'mmm', 'id': '3M Co'}, {'environment_level': 'High', 'social_grade': 'BB', 'governance_level': 'Medium', 'social_level': 'Medium', 'total_score': 1135, 'total_grade': 'BBB', 'social_score': 315, 'weburl': 'https://www.aosmith.com/', 'exchange': 'NEW YORK STOCK EXCHANGE, INC.', 'cik': 91142, 'logo': 'https://static.finnhub.io/logo/73381be8-80eb-11ea-b385-00000000092a.png', 'industry': 'Building', 'governance_score': 310, 'total_level': 'High', 'currency': 'USD', 'governance_grade': 'BB', 'environment_score': 510, 'last_processing_date': '16-04-2022', 'environment_grade': 'A', 'ticker': 'aos', 'id': 'A O Smith Corp'}, {'environment_level': 'High', 'social_grade': 'BB', 'governance_level': 'Medium', 'social_level': 'Medium', 'total_score': 1129, 'total_grade': 'BBB', 'social_score': 324, 'weburl': 'https://www.abiomed.com/', 'exchange': 'NASDAQ NMS - GLOBAL MARKET', 'cik': 815094, 'logo': 'https://static.finnhub.io/logo/8b2cc7cc-80df-11ea-b8c7-00000000092a.png', 'industry': 'Health Care', 'governance_score': 305, 'total_level': 'High', 'currency': 'USD', 'governance_grade': 'BB', 'environment_score': 500, 'last_processing_date': '16-04-2022', 'environment_grade': 'A', 'ticker': 'abmd', 'id': 'ABIOMED Inc'}]
    normalized_esg = esg_data_normalization(esg_data)
    print("\nNormalized esg data:\n")
    print(normalized_esg)
    # [{'company_name': '3M Co', 'environment_grade': 'A', 'environment_score': 526.0, 'normalized_score': 1.0}, 
    # {'company_name': 'A O Smith Corp', 'environment_grade': 'A', 'environment_score': 510.0, 'normalized_score': 0.38461538461538464}, 
    # {'company_name': 'ABIOMED Inc', 'environment_grade': 'A', 'environment_score': 500.0, 'normalized_score': 0.0}]
    transaction_collection = db.collection('transactions')
    transaction_data = collection_to_list_limited(transaction_collection, limit=20)
    print("\nRaw transaction data:\n")
    print(transaction_data)
    # [{'action': 'declined', 'time_completed': '2024-08-31T06:02:27.687Z', 'longitude': -113.807658, 'merchant_name': 'Starbucks', 'latitude': -42.372604, 'customerID': 52, 'amount': 860.27, 'ip_address': '179.152.194.186', 'id': '0'}, 
    #  {'action': 'declined', 'time_completed': '2023-12-07T08:07:20.451Z', 'longitude': -1.121183, 'merchant_name': 'Target', 'latitude': 11.962175, 'customerID': 74, 'amount': 144.53, 'ip_address': '173.64.65.25', 'id': '1'}, 
    #  {'action': 'approved', 'time_completed': '2023-12-13T10:22:26.700Z', 'longitude': 176.909716, 'merchant_name': 'Walmart', 'latitude': 61.823301, 'customerID': 47, 'amount': 962.7, 'ip_address': '46.201.218.108', 'id': '10'}]
    
    User_data = {} # We're going to upload this later
    
    populate_user_transactions(transaction_data, User_data)
    print("\nUser data:\n")
    print(User_data)
    #----------------------------------------------------------------
    print("\nUploading user data to Firestore...\n")
    upload_user_data(User_data) # testing uploading to firebase