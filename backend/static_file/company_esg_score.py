# function to get individual company's esg score
# helper function company_name_matching needed to be implemented correctly

from django.http import JsonResponse
from utils.firebase import db


def company_name_matching(company_name):
    # return the company name that matches the input company name, fuzzy matching, if not found, return None
    return company_name


def get_company_score(company_name):
    if company_name_matching(company_name) is None:
        return JsonResponse({"error": "Company not found"}, status=404)
    else:
        company_name = company_name_matching(company_name)
        # get the company's esg score from Firestore

        # right now the total score is used, but we can edit to make the score more considerate later
        return db.collection("esg").document(company_name).to_dict()["total_score"]
