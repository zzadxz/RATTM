from utils.firebase import db


def collection_to_list(collection_reference) -> list[dict]:
    """Fetches all documents from a specific Firestore collection and returns
    them as a list of dictionaries.

    Args:
        collection_reference example: db.collection('esg')
    """
    documents = collection_reference.stream()
    data_list = []

    for doc in documents:
        doc_data = doc.to_dict()  # Convert each document to a dictionary
        doc_data["id"] = doc.id  # Here, the document id is actually the comapny name
        data_list.append(doc_data)

    return data_list


# This function is for testing purposes
def collection_to_list_limited(collection_reference, limit=2):
    # Use .limit() to fetch only a specified number of documents
    documents = collection_reference.limit(limit).stream()
    data_list = []

    for doc in documents:
        doc_data = doc.to_dict()  # Convert each document to a dictionary
        doc_data["id"] = doc.id  # Optionally include the document ID if needed
        data_list.append(doc_data)

    return data_list


def esg_data_normalization(collection_data: list[dict]):
    # Normalizing the score to be between 0 and 1
    environment_scores = []

    # First file read to get the min and max scores
    for row in collection_data:
        environment_score = float(row["environment_score"])
        environment_scores.append(environment_score)
    min_score = min(environment_scores)
    max_score = max(environment_scores)

    normalized_data = []
    for row in collection_data:
        company_name = row["id"]
        environment_score = float(row["environment_score"])
        environment_grade = row["environment_grade"]
        normalized_score = (environment_score - min_score) / (max_score - min_score)
        data = {
            "company_name": company_name,
            "environment_grade": environment_grade,
            "environment_score": environment_score,
            "normalized_score": normalized_score,
        }
        normalized_data.append(data)
    return normalized_data


def populate_user_transactions(tranaction_data: list[dict], User_data: dict) -> None:
    for transaction in tranaction_data:
        if transaction["customerID"] not in User_data:
            User_data[transaction["customerID"]] = {}
            User_data[transaction["customerID"]]["transactions"] = [transaction]
        else:
            User_data[transaction["customerID"]]["transactions"].append(transaction)


def upload_user_data(User_data: dict) -> None:
    if User_data:
        # Testing for connection to firebase
        try:
            doc = db.collection("test").document("testDoc")
            doc.set({"connected": True})
            print("Firebase is connected, and data was written successfully.")
        except Exception as e:
            print("Connection Error:", e)
        # Now we're uploading the User data
        try:
            for user_id in User_data:
                print(User_data[user_id])
                db.collection("Users").document(str(user_id)).set(User_data[user_id])
            print("User data uploaded successfully.")
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    esg_collection = db.collection("esg")

    esg_data = collection_to_list_limited(esg_collection)  # can set limit=3

    print("\nRaw esg_data:\n")
    print(esg_data)
    normalized_esg = esg_data_normalization(esg_data)
    print("\nNormalized esg data:\n")
    print(normalized_esg)
    transaction_collection = db.collection("transactions")

    transaction_data = collection_to_list_limited(
        transaction_collection
    )  # can set limit=20

    print("\nRaw transaction data:\n")
    print(transaction_data)
    user_data = {}  # We're going to upload this

    populate_user_transactions(transaction_data, user_data)
    print("\nUser data:\n")
    print(user_data)
    # ----------------------------------------------------------------
    print("\nUploading user data to Firestore...\n")
    upload_user_data(user_data)  # testing uploading to firebase, it works!
