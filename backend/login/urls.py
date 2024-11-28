from django.urls import path
from .views import LoginView
from .use_case import LoginUseCase

login_view = LoginView(LoginUseCase())

urlpatterns = [path("get_email/", login_view.get_user_email_from_frontend, name="get_user_email")]
