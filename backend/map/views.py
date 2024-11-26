from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .use_cases import (
    MapUseCase
)

# get map data
def get_map_data(request):
    """
    According to the user id, user_map object is created.
    User map location information is processed and returned.
    """
    user_id = request.session.get("user_id")  or '0'
    user_map = MapUseCase(user_id)
    return JsonResponse(user_map.get_user_all_locations_and_company(), safe=False)
