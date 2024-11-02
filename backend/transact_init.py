from django.shortcuts import render
from django.http import JsonResponse
from esg.views import get_data_from_firestore
from utils.firebase import db
from dotenv import load_dotenv
import csv
import json
import os


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










# import csv
# from firebase_admin import credentials, firestore
# csv_file_path = 'resources/ESG_data.csv'
# # Missing the firestore credentials
# db = firestore.client()
# environment_scores = []
# # First file read to get the min and max scores
# with open(csv_file_path, mode='r') as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         environment_score = float(row['environment_score'])
#         environment_scores.append(environment_score)
# min_score = min(environment_scores)
# max_score = max(environment_scores)
# # Second file read to calculate and upload the data
# with open(csv_file_path, mode='r') as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         # if the score is high, 
#         # then the company has a positive environmental impact
#         company_name = row['name']
#         environment_score = float(row['environment_score'])
#         environment_grade = row['environment_grade']
#         # Normalizing the score to be between 0 and 1
#         normalized_score = (environment_score - min_score) / (max_score - min_score)
#         data = {
#             'company_name': company_name,
#             'environment_grade': environment_grade,
#             'environment_score': environment_score,
#             'normalized_score': normalized_score
#         }
#         # Create or update a document in the 'companies' collection
#         # Use company_name as the document ID to ensure uniqueness
#         db.collection('companies').document(company_name).set(data)


        
if __name__ == '__main__':
    collection = db.collection('esg')
    my_collection_data = collection_to_list_limited(collection, limit=3)
    print(my_collection_data)
    #[{'environment_level': 'High', 'social_grade': 'BB', 'governance_level': 'Medium', 'social_level': 'Medium', 'total_score': 1141, 'total_grade': 'BBB', 'social_score': 310, 'weburl': 'https://www.3m.com/', 'exchange': 'NEW YORK STOCK EXCHANGE, INC.', 'cik': 66740, 'logo': 'https://static.finnhub.io/logo/2a1802fa-80ec-11ea-a0f5-00000000092a.png', 'industry': 'Industrial Conglomerates', 'governance_score': 305, 'total_level': 'High', 'currency': 'USD', 'governance_grade': 'BB', 'environment_score': 526, 'last_processing_date': '16-04-2022', 'environment_grade': 'A', 'ticker': 'mmm', 'id': '3M Co'}, {'environment_level': 'High', 'social_grade': 'BB', 'governance_level': 'Medium', 'social_level': 'Medium', 'total_score': 1135, 'total_grade': 'BBB', 'social_score': 315, 'weburl': 'https://www.aosmith.com/', 'exchange': 'NEW YORK STOCK EXCHANGE, INC.', 'cik': 91142, 'logo': 'https://static.finnhub.io/logo/73381be8-80eb-11ea-b385-00000000092a.png', 'industry': 'Building', 'governance_score': 310, 'total_level': 'High', 'currency': 'USD', 'governance_grade': 'BB', 'environment_score': 510, 'last_processing_date': '16-04-2022', 'environment_grade': 'A', 'ticker': 'aos', 'id': 'A O Smith Corp'}, {'environment_level': 'High', 'social_grade': 'BB', 'governance_level': 'Medium', 'social_level': 'Medium', 'total_score': 1129, 'total_grade': 'BBB', 'social_score': 324, 'weburl': 'https://www.abiomed.com/', 'exchange': 'NASDAQ NMS - GLOBAL MARKET', 'cik': 815094, 'logo': 'https://static.finnhub.io/logo/8b2cc7cc-80df-11ea-b8c7-00000000092a.png', 'industry': 'Health Care', 'governance_score': 305, 'total_level': 'High', 'currency': 'USD', 'governance_grade': 'BB', 'environment_score': 500, 'last_processing_date': '16-04-2022', 'environment_grade': 'A', 'ticker': 'abmd', 'id': 'ABIOMED Inc'}]
    normalized_data = esg_data_normalization(my_collection_data)
    print("\nNormalized data:\n")
    print(normalized_data)
    # [{'company_name': '3M Co', 'environment_grade': 'A', 'environment_score': 526.0, 'normalized_score': 1.0}, 
    # {'company_name': 'A O Smith Corp', 'environment_grade': 'A', 'environment_score': 510.0, 'normalized_score': 0.38461538461538464}, 
    # {'company_name': 'ABIOMED Inc', 'environment_grade': 'A', 'environment_score': 500.0, 'normalized_score': 0.0}]
    
    