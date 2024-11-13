from rest_framework.response import Response
from .use_cases import (
    get_user_all_locations_and_company
    # Note that get_map_data is not imported here because it is from the static_file/map.py file
)

# map data
def get_map_data(request):
    user_id = request.session.get("user_id") 
    return Response(get_user_all_locations_and_company(user_id))
