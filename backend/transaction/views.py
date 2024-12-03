from django.http import JsonResponse
from .abstract_use_case import AbstractTransactionUseCase


# Inject the concrete implementation dynamically
class TransactionView:
    def __init__(self, use_case: AbstractTransactionUseCase):
        self.use_case = use_case

    # Put data in Firestore
    # Endpoint: /transaction/upload
    def upload_data_to_firestore(self, request):
        result = self.use_case.upload_data_to_firestore_use_case()
        if result == 1:
            return JsonResponse({"message": "Data uploaded successfully"}, status=200)
        else:
            return JsonResponse({"error": result}, status=500)

    # Get data from Firestore
    # Endpoint: /transaction/get
    def get_data_from_firestore(self, request):
        user_id = request.session.get("user_id") or "0"
        transactions = self.use_case.get_data_from_firestore_use_case(user_id)
        if isinstance(transactions, str):  # Check if an error message was returned
            return JsonResponse({"error": transactions}, status=500)

        return JsonResponse(transactions, safe=False, status=200)
