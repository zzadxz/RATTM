from .abstract_use_case import AbstractUserUseCase, AbstractIndividualUseCase
from utils.abstract_data_access import AbstractDataAccess
from .calculations import Calculations

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
        self.user_data = {}
        self.calculation = Calculations()


    def get_all_transaction(self): 
        """
        Function to get all transaction data from data_acess.
        """
        transactions = self.data_access.get_table_from_database('transactions')

        return transactions

    def upload_user_data(self): 
        """
        Function to upload individual user data to data_access. 
        """

    # try: 
        transaction_data = self.data_access.get_table_from_database('transactions')
        transaction_data = {str(key): value for key, value in transaction_data.items()}
        # initislize the 100 users in the database 
        for user_id in range(100):
            user_id = str(user_id)
            new_user = IndividualUserUseCase(user_id)
            self.user_data[user_id] = new_user
                
        for transaction in transaction_data: 
            user_id = transaction_data[transaction]['customerID']
            self.user_data[str(user_id)].add_new_transaction(transaction_data[transaction])
        
        # modify the data such that it's {user_id: new_user.data}
        for key in self.user_data.keys():
            temp_value = self.user_data[key].get_data()
            self.user_data[key] = temp_value

        self.data_access.upload_table_to_database(self.user_data, "user")
        #     return 1
    
        # except: 
        #     return 0 

class IndividualUserUseCase(AbstractIndividualUseCase): 
    """
    An implementation of the AbstractUserUseCase. Each instance is a different user.
    """

    def __init__(self, user_id: str):
        """
        Initialize individual user.
        """ 
        self.data = {"transactions": {}}
        self.max_data = 0

    def add_new_transaction(self, transaction):
        """
        Add new transaction to a specific user.
        """
        self.data["transactions"][str(self.max_data)] = transaction
        self.max_data += 1
    
    def get_data(self):
        """
        Getter method for all data.
        """
        return self.data