from .views import UserView
from .use_case import UserUseCase
from django.urls import path 
from utils.firebase_data_access_implementation import FirebaseDataAccess

user_view = UserView(UserUseCase(FirebaseDataAccess))

urlpatterns = [
    path("upload/", user_view.upload_data_to_firestore, name="upload_data")
]