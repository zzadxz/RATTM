from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from static_file.map import get_user_all_locations_and_company
from .use_cases import (
    get_past_12_month_names,
    get_weekly_green_transactions,
    get_weekly_carbon_score,
    get_monthly_green_transactions,
    get_monthly_carbon_score,
    get_total_green_transactions,
    get_top_companies,
    get_total_co2_score,
    get_company_tiers,
    get_co2_score_change,
    get_green_transaction_change
    # Note that get_map_data is not imported here because it is from the static_file/map.py file
)

# endpoint is /login/user_email
@api_view(['POST'])
def get_user_email_from_frontend(request):
    email_to_user_id = {
        "liuyimeng01@gmail.com": 21,
        "gabrielezrathompson@gmail.com": 1,
        "chongwan.w@gmail.com": 4,
        "benrockehenderson@gmail.com": 3,
        "jennifer.r.chiou@gmail.com": 95,
        "callum.sharrock@gmail.com": 0,
        "kiarashsotoudeh@gmail.com": 10
    }
    if request.data in email_to_user_id.keys():
        user_id = email_to_user_id[request.data]
    else:
        user_id = 99

    request.session["user_id"] = user_id
    return Response({"message": f"Got user's email {request.data}", "data": user_id})

def get_months_for_line_graph(request):
    return Response(get_past_12_month_names())

# weekly green transactions for each month - return the last 5 data points as a list
def get_weekly_green_transactions(request):
    user_id = request.session.get("user_id") 
    return Response(get_green_transactions(user_id))

# weekly carbon score for each month - return the last 5 data points as a list
def get_weekly_carbon_score(request):
    user_id = request.session.get("user_id") 
    return Response(get_user_carbon_score(user_id))

# monthly green transactions for each month - return the last 12 data points as a list
def get_monthly_green_transactions(request): # NOT IMPLEMENTED
    user_id = request.session.get("user_id") 
    return Response(get_user_monthly_green_transactions(user_id))

# monthly carbon score for each month - return the last 12 data points as a list
def get_monthly_carbon_score(request):
    user_id = request.session.get("user_id") 
    return Response(get_user_monthly_carbon_score(user_id))

# number of green transactions for each month - the last data point grouped by month
def get_total_green_transactions(request):
    user_id = request.session.get("user_id") 
    return Response(get_user_green_transactions(user_id))

# top 10 companies purchased from, their esg score, and amount purchased from them
def get_top_companies(request):
    user_id = request.session.get("user_id") 
    return Response(get_user_top_companies(user_id))

# total CO2 score
def get_total_co2_score(request):
    user_id = request.session.get("user_id") 
    return Response(get_user_total_co2_score(user_id))

# number of companies from each tier
def get_company_tiers(request):
    user_id = request.session.get("user_id") 
    return Response(get_user_company_tiers(user_id))

# percent increase/decrease of CO2 score
def get_co2_score_change(request): 
    user_id = request.session.get("user_id") 
    return Response(get_user_co2_score_change(user_id))

# percent increase/decrease of green transactions
def get_green_transaction_change(request): 
    user_id = request.session.get("user_id") 
    return Response(get_user_green_transaction_change(user_id))

# map data
def get_map_data(request): # IMPLEMENTED
    user_id = request.session.get("user_id") 
    return Response(get_user_all_locations_and_company(user_id))
