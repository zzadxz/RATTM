from abc import ABC, abstractmethod


class AbstractMapUseCase(ABC):
    """
    Abstract base class defining the the map use cases.
    """

    @abstractmethod
    def __init__(self, user_id):
        """
        Abstract method initiating a use case. 
        """
        self.user_id = user_id

    @abstractmethod
    def get_user_all_locations_and_company(user_id):
        """
        Abstract method returning user's location and compnay of purchase.
        """
        return NotImplementedError