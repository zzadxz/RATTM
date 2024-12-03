from django.urls import path
from .views import (
    MapView
)
from .use_cases import MapUseCase
from utils.firebase_data_access_implementation import FirebaseDataAccess

map_view = MapView(
            MapUseCase(
               FirebaseDataAccess()
            )
        )

urlpatterns = [
    path('get_map_data/', map_view.get_map_data, name='get_map_data')
]