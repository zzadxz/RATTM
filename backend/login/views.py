from rest_framework.decorators import api_view
from rest_framework.response import Response
from .use_case import LoginUseCase 


# endpoint is /login/get_email
@api_view(["POST"])
def get_user_email_from_frontend(request):
    login_use_case = LoginUseCase()
    print(type(request.data))
    user_id = login_use_case.match_email_to_id(request.data)
    request.session["user_id"] = user_id
    return Response({"message": f"Got user's email {request.data}", "data": user_id})
