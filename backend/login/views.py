from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

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

@api_view(['GET'])
# weekly green transactions for each month - return the last 5 data points as a list

# weekly carbon score for each month - return the last 5 data points as a list

# monthly green transactions for each month - return the last 12 data points as a list

# monthly carbon score for each month - return the last 12 data points as a list

# number of green transactions for each month - the last data point grouped by month

# top 10 companies purchased from, their esg score, and amount purchased from them

# total user score

# number of companies from each tier