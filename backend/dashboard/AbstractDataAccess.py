from abc import ABC, abstractmethod

class AbstractDataAccess(ABC):
    @abstractmethod
    def get_table_from_database(self, table_name: str) -> dict:
        raise NotImplementedError