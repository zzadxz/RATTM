from django.urls import path
from .views import (
    MapView
)

# create a view 
map_view = MapView()

urlpatterns = [
    path('get_map_data/', map_view.get_map_data, name='get_map_data')
]