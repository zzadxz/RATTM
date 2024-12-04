from utils.firebase import db
from .abstract_data_access import AbstractDataAccess


class FirebaseDataAccess(AbstractDataAccess):
    """ This class is responsible for handling the data access to the firebase database.
    """
    def get_table_from_database(self, table_to_access: str) -> dict:
        """
        return a dict mapping the key of the firestore collection to the data within its rows
        """
        try:
            docs = db.collection(table_to_access).stream()
            ret = {}
            for doc in docs:
                ret[doc.id] = doc.to_dict()
        except Exception as e:
            ret = None
            print(str(e))
        return ret
    
    def upload_table_to_database(self, data: dict, name: str):
        """
        upload data to the database. specialized for Firestore. 
        """
        for id in data: 
            db.collection(name).document(str(id)).set(data[id])