# env_impact_history/serializers.py
from rest_framework import serializers
from .models import EnvImpactHistory

class EnvImpactHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvImpactHistory
        fields = [
            'user_id',
            'date',
            'company_name',
            'env_score',
            'normalized_env_score',
            'env_grade'
        ]