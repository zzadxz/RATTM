from django.urls import path
from .views import (
    get_weekly_green_transactions,
    get_weekly_carbon_score,
    get_monthly_green_transactions,
    get_monthly_carbon_score,
    get_total_green_transactions,
    get_top_companies,
    get_total_co2_score,
    get_company_tiers,
    get_co2_score_change,
    get_green_transaction_change,
    get_map_data
)
    

urlpatterns = [
    path('get_weekly_green_transactions/', get_weekly_green_transactions, name='get_weekly_green_transactions'),
    path('get_weekly_carbon_score/', get_weekly_carbon_score, name='get_weekly_carbon_score'),
    path('get_monthly_green_transactions/', get_monthly_green_transactions, name='get_monthly_green_transactions'),
    path('get_monthly_carbon_score/', get_monthly_carbon_score, name='get_monthly_carbon_score'),
    path('get_total_green_transactions/', get_total_green_transactions, name='get_total_green_transactions'),
    path('get_top_5_companies/', get_top_companies, name='get_top_companies'),
    path('get_total_co2_score/', get_total_co2_score, name='get_total_co2_score'),
    path('get_company_tiers/', get_company_tiers, name='get_company_tiers'),
    path('get_co2_score_change/', get_co2_score_change, name='get_co2_score_change'),
    path('get_green_transaction_change/', get_green_transaction_change, name='get_green_transaction_change'),
    path('get_map_data/', get_map_data, name='get_map_data')
]