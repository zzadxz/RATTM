from abc import ABC, abstractmethod

class AbstractLoginUseCase(ABC):
    @abstractmethod
    def match_email_to_id(self, email: str) -> str:
        """
        Abstract method to match an email to a user ID.
        Implementations of this method should provide the actual functionality.
        """
        raise NotImplementedError
