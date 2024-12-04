from abstract_use_case import AbstractUserUseCase
from utils.abstract_data_access import AbstractDataAccess
from calculations import 


"""
Implementation note: 
check make sure all necessary functions exist in abstract 
"""

class UserUseCase(AbstractUserUseCase):
    """
    An implementation of the AbstractUserUseCase. 
    Real-time update/fetching is not implemented. 
    """

    def __init__(self, data_access: AbstractDataAccess): 
        """
        Initialize User Use Case. 
        """
        self.data_access = data_access 
        self.all_users = []

    def get_all_esg(self): 
        """
        Function to get all esg data from data_access.
        """
        esg_collection = self.data_access('esg')

        return esg_collection

    def get_all_transaction(self): 
        """
        Function to get all transaction data from data_acess.
        """
        transactions = self.data_access('transactions')

        return transactions

    def upload_user_data(self): 
        """
        Function to upload individual user data to data_access. 
        """
        raise NotImplementedError