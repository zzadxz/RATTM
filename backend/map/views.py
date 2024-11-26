from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .use_cases import (
    MapUseCase
)

class MapView(): 
    """
    This class is the view for the map tab on the website. 
    Methods are used when getting useful purchase information for the map display, given a user. 
    """

    def __init__(self):
        # initialize the view without setting user information
        self.user_id = None 
    
    def get_map_data(self, request):
        """
        According to the user id, user_map object is created.
        User map location information is processed and returned.
        """
        # set user id according to the request 
        self.user_id = request.request.session.get("user_id")  or '0'
        user_map = MapUseCase(self.user_id)
        return JsonResponse(user_map.get_user_all_locations_and_company(), safe=False)
