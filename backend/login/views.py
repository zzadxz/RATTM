from rest_framework.response import Response
from django.http import HttpResponseNotAllowed
from .abstract_use_case import AbstractLoginUseCase


class LoginView:
    def __init__(self, login_use_case: AbstractLoginUseCase):
        self.login_use_case = login_use_case

    def get_user_email_from_frontend(self, request):
        """
        Endpoint: /login/get_email
        Dynamically inject the `login_use_case` dependency.
        """
        if request.method != "POST":
            return HttpResponseNotAllowed(["POST"])
        
        user_id = self.login_use_case.match_email_to_id(request.data)
        request.session["user_id"] = user_id
        return Response({"message": f"Got user's email {request.data}", "data": user_id})