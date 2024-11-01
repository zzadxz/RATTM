# env_impact_history/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnvImpactHistoryViewSet

router = DefaultRouter()
router.register(r'env_impact_history', EnvImpactHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]