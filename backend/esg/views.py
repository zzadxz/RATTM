from django.shortcuts import render
from django.http import JsonResponse
from utils.firebase import db
from dotenv import load_dotenv
import csv
import json
import os

class ESGView:
# endpoint: /esg/upload
    def upload_data_to_firestore(self, request):
        load_dotenv()
        esg_path = os.getenv('ESG_PATH')
        with open(esg_path, 'r') as file:
            data = json.load(file)
        
        try:
            doc = db.collection('test').document('testDoc')
            doc.set({'connected': True})
            print("Firebase is connected, and data was written successfully.")
        except Exception as e:
            print("Connection Error:", e)

        try:
            if db.collection('esg').get():
                db.collection('esg').delete()
            for info in data: 
                company_name = info.get("name")
                entries = {k: v for k, v in info.items() if k != "name"}
                db.collection('esg').document(str(company_name)).set(entries)
            return JsonResponse({'message': 'Esg data uploaded successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


    # as we move forward, this can be deleted 
    # endpoint: /esg/get
    def get_data_from_firestore(self, request):
        try:
            docs = db.collection('esg').stream()
            all_esg = []
            for doc in docs:
                all_esg.append(doc.to_dict())

            return JsonResponse(all_esg, safe=False, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

    # get indivudual esg scores for company, need to be updated 
    # end point: /esg/get/<company_name>
    def get_individual_company_score(self, company_name):
        try:
            results = db.collection('esg').where('merchant_name', '==', company_name).limit(1).stream()
            return JsonResponse(results, safe=False, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)