from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from transaction.models import Transaction

from transaction.serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [AllowAny]