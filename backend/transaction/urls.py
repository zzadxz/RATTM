from django.urls import path
from .views import TransactionView
from .abstract_use_case import AbstractTransactionUseCase
from .calculations import Calculations
from utils.firebase_data_access_implementation import FirebaseDataAccess

transaction_view = TransactionView(AbstractTransactionUseCase(Calculations(), FirebaseDataAccess()))

urlpatterns = [
    path("upload/", transaction_view.upload_data_to_firestore, name="upload_data"),
    path("get/", transaction_view.get_data_from_firestore, name="get_data"),
]
