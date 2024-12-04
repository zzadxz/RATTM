from abc import ABC, abstractmethod

class AbstractUserUseCase(ABC):
    """
    Abstract base class defining the contract for user use cases.
    """

    @abstractmethod
    def upload_user_data(self):
        """
        Abstract method for uploading user data to Firestore's user collection.
        Implementations should handle uploading user data.
        """
        raise NotImplementedError

class AbstractIndividualUseCase(ABC): 
    """
    Abstract base class for defining each user use case.
    """

    @abstractmethod
    def populate_user_transactions(self):
        """
        Abstract method for populating user data with transaction data from Firestore.
        Implementations should handle writing user data to Firestore.
        """
        raise NotImplementedError