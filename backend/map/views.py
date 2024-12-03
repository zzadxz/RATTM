from django.http import JsonResponse
from .abstract_use_case import AbstractMapUseCase

class MapView(): 
    """
    This class is the view for the map tab on the website. 
    Methods are used when getting useful purchase information for the map display, given a user. 
    """

    def __init__(self, user_map: AbstractMapUseCase):
        # initialize the view without setting user information
        self.user_map = user_map
    
    def get_map_data(self, request):
        """
        According to the user id, user_map object is created.
        User map location information is processed and returned.
        """
        # set user id according to the request 
        user_id = request.session.get("user_id")  or '0'
        return JsonResponse(self.user_map.get_user_all_locations_and_company(user_id), safe=False)
