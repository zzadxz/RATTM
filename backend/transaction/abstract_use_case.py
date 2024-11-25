from abc import ABC, abstractmethod


class AbstractTransactionUseCase(ABC):
    """
    Abstract base class defining the contract for transaction use cases.
    """

    @abstractmethod
    def upload_data_to_firestore_use_case(self):
        """
        Abstract method for uploading data to Firestore.
        Implementations should handle writing transaction data to Firestore.
        """
        pass

    @abstractmethod
    def get_data_from_firestore_use_case(self):
        """
        Abstract method for retrieving transaction data from Firestore.
        Implementations should handle fetching and returning transaction data.
        """
        pass
