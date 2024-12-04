from django.urls import path
from .views import ESGView

esg_views = ESGView()
urlpatterns = [
    path('get/', esg_views.get_data_from_firestore, name='get_data'),
    # individual score will be in static_file
]