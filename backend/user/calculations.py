class Calculations: 
    """
    Calculations to support with managing user data and firestore. 
    """
    
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
            doc_data['id'] = doc.id   # Here, the document id is actually the comapny name
            data_list.append(doc_data)
        
        return data_list
