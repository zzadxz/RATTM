from django.urls import path
from .view import upload_data_to_firestore, get_data_from_firestore

urlpatterns = [
    path('upload/', upload_data_to_firestore, name='upload_data'),
    path('get/', get_data_from_firestore, name='get_data'),
]