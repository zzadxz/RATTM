from django.urls import path
from .views import (
    get_line_graph_data,
    get_total_green_transactions,
    get_this_month_green_transactions,
    get_top_5_companies,
    get_total_co2_score,
    get_this_month_co2_score,
    get_company_tiers,
    get_co2_score_change,
    get_green_transaction_change,
)
    
urlpatterns = [
    path('get_line_graph_data/', get_line_graph_data, name='get_line_graph_data'),
    path('get_this_month_green_transactions/', get_this_month_green_transactions, name='get_this_month_green_transactions'),
    path('get_total_green_transactions/', get_total_green_transactions, name='get_total_green_transactions'),
    path('get_top_5_companies/', get_top_5_companies, name='get_top_5_companies'),
    path('get_total_co2_score/', get_total_co2_score, name='get_total_co2_score'),
    path('get_this_month_co2_score/', get_this_month_co2_score, name='get_this_month_co2_score'),
    path('get_company_tiers/', get_company_tiers, name='get_company_tiers'),
    path('get_co2_score_change/', get_co2_score_change, name='get_co2_score_change'),
    path('get_green_transaction_change/', get_green_transaction_change, name='get_green_transaction_change'),
]