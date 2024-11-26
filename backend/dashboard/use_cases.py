from static_file.company_esg_score import company_name_matching, get_company_score
from .calculations import Calculations
from utils.abstract_data_access import AbstractDataAccess
from datetime import date, datetime

class DashboardUseCases:
    """DashboardUseCases class is responsible for handling the business logic of the dashboard.
    """
    def __init__(self, calculations: Calculations, data_access: AbstractDataAccess):
        self.calculations = calculations
        self.data_access = data_access
    def past_12_month_names() -> list[str]:
        """
        Returns a reordering of ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] based on the current month
        """
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        # Get the current month index (Jan=0, Dec=11)
        current_month_index = datetime.now().month - 2
        
        # Re-arrange the months so it starts from the current month
        reordered_months = months[current_month_index:] + months[:current_month_index]
        
        return reordered_months


    def monthly_carbon_scores(user_id) -> list[int]:
        """
        Returns list of length 12 of carbon scores each month.
        """
        user_transactions = self.data_access.get_table_from_database('Users')[user_id]['transactions']
        esg_data = self.data_access.get_table_from_database('esg')
        # reverse the list so that the most recent data point is the last element
        return self.calculations.calculate_historical_scores(user_transactions, esg_data)[::-1]


    def monthly_green_transactions(user_id) -> list[int]:
        """
        Returns list of length 12 of # of green transactions each month.
        """
        user_transactions = self.data_access.get_table_from_database('Users')[user_id]['transactions']
        esg_data = self.data_access.get_table_from_database('esg')
        return self.calculations.calculate_historical_scores(user_transactions, esg_data)[::-1]
        

    def total_green_transactions(user_id) -> int:
        """
        Return total number of green transactions this month. 
        """
        user_transactions = self.data_access.get_table_from_database('Users')[user_id]['transactions']
        esg_data = self.data_access.get_table_from_database('esg')
        return self.calculations.calculate_total_green_transactions(user_transactions, esg_data)
        

    def this_month_green_transactions(user_id) -> int:
        """
        Return total number of green transactions this month. 
        """
        user_transactions = self.data_access.get_table_from_database('Users')[user_id]['transactions']
        esg_data = self.data_access.get_table_from_database('esg')
        return self.calculations.calculate_historical_green_transactions(user_transactions, esg_data)[0]
        

    def top_5_companies(user_id) -> dict:
        """
        Returns in dict format:  { 'Company Name' : str, 'ESG Score' : int, 'Amount Spent' : int }
        """
        user_transactions = self.data_access.get_table_from_database('Users')[user_id]['transactions']
        esg_data = self.data_access.get_table_from_database('esg')
        return self.calculate.find_most_purchased_companies(user_transactions, esg_data)


    def total_co2_score(user_id) -> int:
        """
        Returns CO2 score for the past year.
        """
        user_transactions = self.data_access.get_table_from_database('Users')[user_id]['transactions']
        esg_data = self.data_access.get_table_from_database('esg')
        monthly_scores = [score for score in self.calculations.calculate_historical_scores(user_transactions, esg_data)
                            if score is not None]
        return int(sum(monthly_scores) / len(monthly_scores))


    def this_month_co2_score(user_id) -> int:
        """
        Returns CO2 score for this month.
        """
        user_transactions = self.data_access.get_table_from_database('Users')[user_id]['transactions']
        esg_data = self.data_access.get_table_from_database('esg')
        return self.calculations.calculate_historical_scores(user_transactions, esg_data)[0]


    def company_tiers(user_id) -> list[int]:
        """
        Returns list of length 4, where the first index is the number of companies in the highest tier.
        """
        user_transactions = self.data_access.get_table_from_database('Users')[user_id]['transactions']
        esg_data = self.data_access.get_table_from_database('esg')
        return self.calculations.find_companies_in_each_tier(user_transactions, esg_data)


    def co2_score_change(user_id) -> int:
        """
        Returns the difference between last month and this month's CO2 score.
        """
        user_transactions = self.data_access.get_table_from_database('Users')[user_id]['transactions']
        esg_data = self.data_access.get_table_from_database('esg')
        monthly_scores = self.calculations.calculate_historical_scores(user_transactions, esg_data)

        if monthly_scores[0] is None or monthly_scores[1] is None:
            return 0
        return int(monthly_scores[0] - monthly_scores[1])
        

    def green_transaction_change(user_id) -> int:
        """
        Returns the difference between last month and this month's # of green transactions.
        """
        user_transactions = self.data_access.get_table_from_database('Users')[user_id]['transactions']
        esg_data = self.data_access.get_table_from_database('esg')
        monthly_green_transactions = self.calculations.calculate_historical_green_transactions(user_transactions, esg_data)
        if monthly_green_transactions[0] is None or monthly_green_transactions[1] is None:
            return 0
        return int(monthly_green_transactions[0] - monthly_green_transactions[1])
