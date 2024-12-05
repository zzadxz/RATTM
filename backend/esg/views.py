from django.shortcuts import render
from django.http import JsonResponse
from utils.firebase import db
from dotenv import load_dotenv
import csv
import json
import os

class ESGView:
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
        