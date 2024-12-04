from abc import ABC, abstractmethod

#
class AbstractDataAccess(ABC):
    """
    Abstract class for the data access layer. 
    """

    @abstractmethod
    def get_table_from_database(self, table_name: str) -> dict:
        """
        Get data from the database. 
        """

        raise NotImplementedError
    
    @abstractmethod 
    def upload_table_to_database(self, data: dict, table_name: str): 
        """
        Upload data to the database. 
        """

        raise NotImplementedError