from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .use_cases import match_email_to_id

# endpoint is /login/user_email
@api_view(['POST'])
def get_user_email_from_frontend(request):
    request.session["user_id"] = match_email_to_id(request.data)
    return Response({"message": f"Got user's email {request.data}", "data": user_id})