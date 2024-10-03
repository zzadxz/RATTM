from rest_framework import routers

from transaction.viewsets import TransactionViewSet

router = routers.SimpleRouter()

router.register(r'transaction', TransactionViewSet, basename="transaction")

urlpatterns = router.urls