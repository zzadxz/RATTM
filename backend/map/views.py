from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .use_cases import get_user_all_locations_and_company


# map data
def get_map_data(request):
    user_id = request.session.get("user_id") or "0"
    return JsonResponse(get_user_all_locations_and_company(user_id), safe=False)
