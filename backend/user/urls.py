from views import UserView
from abstract_use_case import AbstractUserUseCase
from django.urls import path 

user_view = UserView(AbstractUserUseCase())

urlpatterns = [
    path("upload/", user_view.upload_data_to_firestore, name="upload_data")
]