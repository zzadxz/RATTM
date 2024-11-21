from .firebase import db


def get_table_from_firebase(table_to_access: str):
    """
    Return a dict mapping the key of the firestore collection to the data within its rows.
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
