from abstract_use_case import AbstractUserUseCase
from django.http import JsonResponse

class UserView: 
    """
    User view
    """
    def __init__(self, user_case: AbstractUserUseCase):
        self.use_case = user_case
    
    # endpoint: /user/upload 
    def upload_data_to_firestore(self, request): 
        result = self.use_case.upload_user_data()
        if result == 1: 
            return JsonResponse({"message": "Data uploaded successfully"}, status=200)
        else:
            return JsonResponse({"error": result}, status=500)
    