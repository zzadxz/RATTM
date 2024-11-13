from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .use_cases import (
    past_12_month_names,
    weekly_carbon_scores,
    monthly_carbon_scores,
    weekly_green_transactions,
    monthly_green_transactions,
    total_green_transactions,
    top_5_companies,
    total_co2_score,
    company_tiers,
    co2_score_change,
    green_transaction_change
)
from random import randint

def get_months_for_line_graph(request):
    return Response(get_past_12_month_names())

# weekly carbon score for each month - return the last 5 data points as a list
def get_weekly_carbon_score(request):
    user_id = request.session.get("user_id") 
    return Response(weekly_carbon_scores(user_id))

# monthly carbon score for each month - return the last 12 data points as a list
def get_monthly_carbon_score(request):
    user_id = request.session.get("user_id") 
    return Response(monthly_carbon_score(user_id))

# weekly green transactions for each month - return the last 5 data points as a list
def get_weekly_green_transactions(request):
    user_id = request.session.get("user_id") 
    return Response(weekly_green_transactions(user_id))

# monthly green transactions for each month - return the last 12 data points as a list
def get_monthly_green_transactions(request): # NOT IMPLEMENTED
    user_id = request.session.get("user_id") 
    return Response(monthly_green_transactions(user_id))

# number of green transactions for each month - the last data point grouped by month
def get_total_green_transactions(request):
    user_id = request.session.get("user_id") 
    return Response(total_green_transactions(user_id))

# top 10 companies purchased from, their esg score, and amount purchased from them
def get_top_companies(request):
    user_id = request.session.get("user_id") 
    return Response(top_5_companies(user_id))

# total CO2 score
def get_total_co2_score(request):
    user_id = request.session.get("user_id") 
    return Response(total_co2_score(user_id))

# number of companies from each tier
def get_company_tiers(request):
    user_id = request.session.get("user_id") 
    return Response(company_tiers(user_id))

# percent increase/decrease of CO2 score
def get_co2_score_change(request): 
    user_id = request.session.get("user_id") 
    return Response(co2_score_change(user_id))

# percent increase/decrease of green transactions
def get_green_transaction_change(request): 
    user_id = request.session.get("user_id") 
    return Response(green_transaction_change(user_id))