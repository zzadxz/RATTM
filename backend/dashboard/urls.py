from django.urls import path
from .views import DashboardView
from .use_cases import DashboardUseCases
from .calculations import Calculations
from utils.firebase_data_access_implementation import FirebaseDataAccess
# This is a builder for dashboard
views = DashboardView(
            DashboardUseCases(
                Calculations(), FirebaseDataAccess()
            )
        )
urlpatterns = [
    path('get_line_graph_data/', views.get_line_graph_data, name='get_line_graph_data'),
    path('get_this_month_green_transactions/', views.get_this_month_green_transactions, name='get_this_month_green_transactions'),
    path('get_total_green_transactions/', views.get_total_green_transactions, name='get_total_green_transactions'),
    path('get_top_5_companies/', views.get_top_5_companies, name='get_top_5_companies'),
    path('get_total_co2_score/', views.get_total_co2_score, name='get_total_co2_score'),
    path('get_this_month_co2_score/', views.get_this_month_co2_score, name='get_this_month_co2_score'),
    path('get_company_tiers/', views.get_company_tiers, name='get_company_tiers'),
    path('get_co2_score_change/', views.get_co2_score_change, name='get_co2_score_change'),
    path('get_green_transaction_change/', views.get_green_transaction_change, name='get_green_transaction_change'),
]