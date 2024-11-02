from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# create 
# documentation: https://docs.djangoproject.com/en/5.1/topics/class-based-views/
# class-based view 
# def create_user(request):

@api_view(['POST'])
def get_user_email_from_frontend(request):
    print(request.data)
    return Response({"message": "Got user's email", "data": request.data})
    