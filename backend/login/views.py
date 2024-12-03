import json
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponseNotAllowed
from .abstract_use_case import AbstractLoginUseCase
from django.views.decorators.csrf import csrf_exempt

class LoginView:
    def __init__(self, login_use_case: AbstractLoginUseCase):
        self.login_use_case = login_use_case

    @csrf_exempt
    def get_user_email_from_frontend(self, request):
        """
        Endpoint: /login/get_email
        Dynamically inject the `login_use_case` dependency.
        """
        if request.method != "POST":
            return HttpResponseNotAllowed(["POST"])
        
        body = json.loads(request.body)
        user_email = body.get("userEmail")
        user_id = self.login_use_case.match_email_to_id(user_email)
        request.session["user_id"] = user_id
        print(user_id)
        return JsonResponse({"message": f"Got user's email {user_email}", "data": user_id})
