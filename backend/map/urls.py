from django.urls import path
from .views import (
    get_map_data
)
    
urlpatterns = [
    path('get_map_data/', get_map_data, name='get_map_data')
]