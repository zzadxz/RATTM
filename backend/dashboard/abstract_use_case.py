from abc import ABC, abstractmethod

class AbstractDashboardUseCases(ABC):
    """
    Abstract class defining the methods for the dashboard use cases.
    """

    @abstractmethod
    def past_12_month_names(self) -> list[str]:
        """
        Returns a reordering of ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] based on the current month.
        """
        raise NotImplementedError

    @abstractmethod
    def monthly_carbon_scores(self, user_id) -> list[int]:
        """
        Returns list of length 12 of carbon scores each month.
        """
        raise NotImplementedError

    @abstractmethod
    def monthly_green_transactions(self, user_id) -> list[int]:
        """
        Returns list of length 12 of # of green transactions each month.
        """
        raise NotImplementedError

    @abstractmethod
    def total_green_transactions(self, user_id) -> int:
        """
        Return total number of green transactions this month.
        """
        raise NotImplementedError

    @abstractmethod
    def this_month_green_transactions(self, user_id) -> int:
        """
        Return total number of green transactions this month.
        """
        raise NotImplementedError

    @abstractmethod
    def top_5_companies(self, user_id) -> dict:
        """
        Returns in dict format: { 'Company Name' : str, 'ESG Score' : int, 'Amount Spent' : int }.
        """
        raise NotImplementedError

    @abstractmethod
    def total_co2_score(self, user_id) -> int:
        """
        Returns CO2 score for the past year.
        """
        raise NotImplementedError

    @abstractmethod
    def this_month_co2_score(self, user_id) -> int:
        """
        Returns CO2 score for this month.
        """
        raise NotImplementedError

    @abstractmethod
    def company_tiers(self, user_id) -> list[int]:
        """
        Returns list of length 4, where the first index is the number of companies in the highest tier.
        """
        raise NotImplementedError

    @abstractmethod
    def co2_score_change(self, user_id) -> int:
        """
        Returns the difference between last month and this month's CO2 score.
        """
        raise NotImplementedError

    @abstractmethod
    def green_transaction_change(self, user_id) -> int:
        """
        Returns the difference between last month and this month's # of green transactions.
        """
        raise NotImplementedError