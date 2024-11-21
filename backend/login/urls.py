from django.urls import path
from .views import get_user_email_from_frontend


urlpatterns = [path("get_email/", get_user_email_from_frontend, name="get_user_email")]
