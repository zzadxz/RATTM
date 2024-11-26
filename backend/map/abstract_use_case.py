from abc import ABC, abstractmethod


class AbstractMapUseCase(ABC):
    """
    Abstract base class defining the the map use cases.
    """

    @abstractmethod
    def __init__(self):
        """
        Abstract method initiating a use case. 
        """
        raise NotImplementedError

    @abstractmethod
    def get_user_all_locations_and_company(user_id):
        """
        Abstract method returning user's location and compnay of purchase.
        """
        return NotImplementedError