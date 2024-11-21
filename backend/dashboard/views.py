from django.http import JsonResponse
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
    green_transaction_change,
)


def get_line_graph_data(request):
    """
    monthly carbon score, green transactions, and month names for each month - 
    return the last 12 data points as a list
    """
    user_id = request.session.get("user_id") or "0"
    data = {
        "months": past_12_month_names(),
        "carbon_scores": monthly_carbon_scores(user_id),
        "green_transactions": monthly_green_transactions(user_id),
    }
    return JsonResponse(data, safe=False)


def get_this_month_green_transactions(request):
    """
    number of green transactions for each month - the last data point grouped by month
    """
    user_id = request.session.get("user_id") or "0"
    return JsonResponse(this_month_green_transactions(user_id), safe=False)


def get_total_green_transactions(request):
    """
    number of green transactions for all time
    """
    user_id = request.session.get("user_id") or "0"
    return JsonResponse(total_green_transactions(user_id), safe=False)


def get_top_5_companies(request):
    """
    top 5 companies purchased from, their esg score, and amount purchased from them
    """
    user_id = request.session.get("user_id") or "0"
    return JsonResponse(top_5_companies(user_id), safe=False)


def get_total_co2_score(request):
    """
    total co2 score
    """
    user_id = request.session.get("user_id") or "0"
    return JsonResponse(total_co2_score(user_id), safe=False)


def get_this_month_co2_score(request):
    """
    this month CO2 score
    """
    user_id = request.session.get("user_id") or "0"
    return JsonResponse(this_month_co2_score(user_id), safe=False)


def get_company_tiers(request):
    """
    number of companies from each tier
    """
    user_id = request.session.get("user_id") or "0"
    return JsonResponse(company_tiers(user_id), safe=False)


def get_co2_score_change(request):
    """
    increase/decrease of CO2 score
    """
    user_id = request.session.get("user_id") or "0"
    return JsonResponse(co2_score_change(user_id), safe=False)


def get_green_transaction_change(request):
    """
    percent increase/decrease of green transactions
    """
    user_id = request.session.get("user_id") or "0"
    return JsonResponse(green_transaction_change(user_id), safe=False)
