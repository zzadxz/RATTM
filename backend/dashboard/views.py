from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .use_cases import (
    past_12_month_names,
    monthly_carbon_scores,
    monthly_green_transactions,
    this_month_green_transactions,
    total_green_transactions,
    top_5_companies,
    total_co2_score,
    this_month_co2_score,
    company_tiers,
    co2_score_change,
    green_transaction_change
)
from random import randint


# monthly carbon score, green transactions, and month names for each month - return the last 12 data points as a list
def get_line_graph_data(request):
    user_id = request.session.get("user_id") or '0'
    data = {
        "months": past_12_month_names(),
        "carbon_scores": monthly_carbon_scores(user_id),
        "green_transactions": monthly_green_transactions(user_id),
    }
    return JsonResponse(data, safe=False)


# number of green transactions for each month - the last data point grouped by month
def get_this_month_green_transactions(request):
    user_id = request.session.get("user_id") or '0'
    return JsonResponse(this_month_green_transactions(user_id), safe=False)

# number of green transactions for all time
def get_total_green_transactions(request):
    user_id = request.session.get("user_id") or '0'
    return JsonResponse(total_green_transactions(user_id), safe=False)


# top 5 companies purchased from, their esg score, and amount purchased from them
def get_top_5_companies(request):
    user_id = request.session.get("user_id") or '0'
    return JsonResponse(top_5_companies(user_id), safe=False)

# total CO2 score
def get_total_co2_score(request):
    user_id = request.session.get("user_id") or '0'
    return JsonResponse(total_co2_score(user_id), safe=False)

# this month CO2 score
def get_this_month_co2_score(request):
    user_id = request.session.get("user_id") or '0'
    return JsonResponse(this_month_co2_score(user_id), safe=False)

# number of companies from each tier
def get_company_tiers(request):
    user_id = request.session.get("user_id") or '0'
    return JsonResponse(company_tiers(user_id), safe=False)

# increase/decrease of CO2 score
def get_co2_score_change(request): 
    user_id = request.session.get("user_id") or '0'
    return JsonResponse(co2_score_change(user_id), safe=False)

# percent increase/decrease of green transactions
def get_green_transaction_change(request): 
    user_id = request.session.get("user_id") or '0'
    return JsonResponse(green_transaction_change(user_id), safe=False)
