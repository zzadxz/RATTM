from django.urls import path
from .views import TransactionView
from .use_case import TransactionUseCase

transaction_view = TransactionView(TransactionUseCase())

urlpatterns = [
    path("upload/", transaction_view.upload_data_to_firestore, name="upload_data"),
    path("get/", transaction_view.get_data_from_firestore, name="get_data"),
]
