from utils.firebase import db
from utils.data_access import get_table_from_firebase
from static_file.company_esg_score import company_name_matching, get_company_score
from static_file.map import get_all_locations_and_company
from datetime import date

# Note that get_map is not needed here beacuse it can be imported from static.get_user_all_locations_and_company

# Added this function here from static_file.map
def get_user_all_locations_and_company(user_id):
    user_transactions = get_table_from_firebase('Users')[user_id]['transactions']
    esg_data = get_table_from_firebase('esg')
    get_all_locations_and_company(user_transactions, esg_data)