# env_impact_history/views.py
from rest_framework import viewsets
from .models import EnvImpactHistory
from .serializers import EnvImpactHistorySerializer

class EnvImpactHistoryViewSet(viewsets.ModelViewSet):
    queryset = EnvImpactHistory.objects.all()
    serializer_class = EnvImpactHistorySerializer