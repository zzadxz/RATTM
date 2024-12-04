from django.http import JsonResponse
from utils.firebase import db
from dotenv import load_dotenv
import json
import os
from .abstract_use_case import AbstractTransactionUseCase
from utils.abstract_data_access import AbstractDataAccess
from .calculations import Calculations

class TransactionUseCase(AbstractTransactionUseCase):
    def __init__(self, calculations: Calculations, data_access: AbstractDataAccess):
        self.calculations = calculations
        self.data_access = data_access
    
    # Put data in Firestore
    # endpoint: /transaction/upload
    def upload_data_to_firestore_use_case(self):
        # obtained from script of transaction_data_edits jupyter notebook
        ip = {
            "143.15.148.251": 0,
            "36.183.96.60": 1,
            "47.174.183.224": 2,
            "45.190.2.193": 3,
            "179.168.100.117": 4,
            "188.202.11.235": 5,
            "14.41.55.238": 6,
            "141.10.185.244": 7,
            "34.60.202.13": 8,
            "12.36.236.135": 9,
            "181.218.85.144": 10,
            "6.79.75.134": 11,
            "170.106.226.176": 12,
            "154.227.167.168": 13,
            "87.118.210.100": 14,
            "54.34.103.141": 15,
            "22.108.183.13": 16,
            "5.121.64.74": 17,
            "95.205.84.112": 18,
            "39.150.106.213": 19,
            "92.12.199.60": 20,
            "164.101.33.162": 21,
            "3.165.137.53": 22,
            "165.196.127.137": 23,
            "82.5.48.207": 24,
            "68.108.209.164": 25,
            "218.61.158.249": 26,
            "138.98.175.187": 27,
            "202.123.163.19": 28,
            "71.185.127.120": 29,
            "83.48.142.206": 30,
            "8.244.26.229": 31,
            "55.72.113.232": 32,
            "87.252.159.130": 33,
            "209.171.243.179": 34,
            "27.119.152.120": 35,
            "201.38.142.229": 36,
            "88.144.35.85": 37,
            "128.219.138.250": 38,
            "104.31.222.118": 39,
            "109.152.80.196": 40,
            "159.54.236.125": 41,
            "34.180.122.225": 42,
            "139.159.109.104": 43,
            "191.21.87.142": 44,
            "45.236.64.19": 45,
            "210.161.102.100": 46,
            "46.201.218.108": 47,
            "205.91.79.103": 48,
            "74.162.199.186": 49,
            "99.240.61.101": 50,
            "106.18.72.102": 51,
            "179.152.194.186": 52,
            "13.240.99.200": 53,
            "34.38.220.59": 54,
            "39.8.86.78": 55,
            "64.88.31.187": 56,
            "95.57.199.73": 57,
            "184.228.97.227": 58,
            "133.234.165.82": 59,
            "54.103.0.113": 60,
            "18.110.181.52": 61,
            "7.12.5.151": 62,
            "107.144.93.145": 63,
            "9.179.103.60": 64,
            "42.23.164.49": 65,
            "175.53.10.84": 66,
            "189.86.30.245": 67,
            "220.154.228.169": 68,
            "204.212.138.101": 69,
            "135.171.93.232": 70,
            "163.147.94.147": 71,
            "99.72.59.81": 72,
            "191.231.10.2": 73,
            "173.64.65.25": 74,
            "126.113.57.231": 75,
            "130.249.211.177": 76,
            "12.194.5.123": 77,
            "77.40.41.71": 78,
            "11.113.210.247": 79,
            "138.228.75.216": 80,
            "175.79.105.155": 81,
            "149.193.51.17": 82,
            "84.192.205.135": 83,
            "28.162.128.41": 84,
            "121.83.25.236": 85,
            "208.207.125.243": 86,
            "219.97.230.11": 87,
            "18.206.33.3": 88,
            "38.210.78.206": 89,
            "71.139.201.121": 90,
            "176.93.132.169": 91,
            "113.185.153.63": 92,
            "222.191.228.75": 93,
            "16.40.44.202": 94,
            "84.165.156.117": 95,
            "126.250.62.151": 96,
            "113.52.124.204": 97,
            "96.49.64.131": 98,
            "109.76.11.85": 99,
        }

        docs = db.collection("transactions").limit(1).get()

        if not docs:
            load_dotenv()
            mock_json_path = os.getenv("MOCK_JSON_PATH")
            with open(mock_json_path, "r") as file:
                data = json.load(file)

            data = data["data"]

            ip_to_user = {}
            user_id = 0

            try:
                doc = db.collection("test").document("testDoc")
                doc.set({"connected": True})
                print("Firebase is connected, and data was written successfully.")
            except Exception as e:
                print("Connection Error:", e)

            for i in ip:
                ip_to_user[i] = user_id
                user_id += 1

            for i in data:
                i["customerID"] = ip_to_user[i["ip_address"]]

            try:
                for transaction in data:
                    transaction_id = transaction[
                        "transactionID"
                    ]  # Get the transaction ID
                    # Remove 'transactionID' from the dictionary to avoid duplication in Firestore
                    transaction_data = {
                        k: v for k, v in transaction.items() if k != "transactionID"
                    }
                    # Use transaction_id as the document ID and add the rest as the document data
                    db.collection("transactions").document(str(transaction_id)).set(
                        transaction_data
                    )
                return 1

            except Exception as e:
                return str(e)

    # Get data from Firestore
    # endpoint: /transaction/get
    def get_data_from_firestore_use_case(self, user_id: str):
        user_transactions = self.data_access.get_table_from_database('users')[user_id]['transactions']
        esg_data = self.data_access.get_table_from_database('esg')
        for t in user_transactions:
            score = self.calculations.get_company_env_score(t, esg_data)
            t['esg_score'] = round(score, 2) if score != 0 else "N/A"
        return user_transactions

    