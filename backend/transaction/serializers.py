""" 
NOT IMPLEMENTED
-> converts django models/other complex data types into jsons/simple data types
"""
from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'transaction_id',
            'client_id',
            'date',
            'company_name',
            'location_latitude',
            'location_longitude',
            'transaction_amount'
        ]

class ESGSerializer(serializers.ModelSerializer)