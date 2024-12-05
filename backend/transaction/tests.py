import unittest
from unittest.mock import MagicMock, patch, mock_open
from django.test import RequestFactory
from django.http import JsonResponse

from .views import TransactionView
from .use_case import TransactionUseCase
from .abstract_use_case import AbstractTransactionUseCase
from .calculations import Calculations

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.mock_use_case = MagicMock(spec=AbstractTransactionUseCase)
        self.view = TransactionView(use_case=self.mock_use_case)
        self.factory = RequestFactory()

    def test_upload_data_to_firestore_success(self):
        self.mock_use_case.upload_data_to_firestore_use_case.return_value = 1
        request = self.factory.post('/transaction/upload')
        response = self.view.upload_data_to_firestore(request)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"message": "Data uploaded successfully"})

    def test_upload_data_to_firestore_failure(self):
        self.mock_use_case.upload_data_to_firestore_use_case.return_value = 'Error uploading data'
        request = self.factory.post('/transaction/upload')
        response = self.view.upload_data_to_firestore(request)
        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(response.content, {"error": "Error uploading data"})

    def test_get_data_from_firestore_success(self):
        transactions = [{'merchant_name': 'Company A', 'esg_score': 85.5}]
        self.mock_use_case.get_data_from_firestore_use_case.return_value = transactions
        request = self.factory.get('/transaction/get')
        request.session = {'user_id': '1'}
        response = self.view.get_data_from_firestore(request)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, transactions)

    def test_get_data_from_firestore_failure(self):
        self.mock_use_case.get_data_from_firestore_use_case.return_value = 'Error retrieving data'
        request = self.factory.get('/transaction/get')
        request.session = {'user_id': '1'}
        response = self.view.get_data_from_firestore(request)
        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(response.content, {"error": "Error retrieving data"})

    def assertJSONEqual(self, raw_content, expected_data):
        import json
        content = json.loads(raw_content)
        self.assertEqual(content, expected_data)


class UseCaseTests(unittest.TestCase):
    def setUp(self):
        self.mock_calculations = MagicMock(spec=Calculations)
        self.mock_data_access = MagicMock()
        self.use_case = TransactionUseCase(
            calculations=self.mock_calculations,
            data_access=self.mock_data_access
        )

    @patch('transaction.use_case.db')
    @patch('transaction.use_case.os.getenv')
    @patch('transaction.use_case.open', new_callable=mock_open, read_data='{"data": []}')
    @patch('transaction.use_case.json.load')
    def test_upload_data_to_firestore_use_case_success(self, mock_json_load, mock_open_file, mock_getenv, mock_db):
        mock_db.collection.return_value.limit.return_value.get.return_value = []
        mock_getenv.return_value = 'mock_json_path'
        mock_json_load.return_value = {'data': []}

        result = self.use_case.upload_data_to_firestore_use_case()
        self.assertEqual(result, 1)

    """
    def test_get_data_from_firestore_use_case(self):
        user_id = '1'
        transactions = [{'merchant_name': 'Company A'}]
        esg_data = {'Company A': {'environment_score': 85.5}}

        self.mock_data_access.get_table_from_database.side_effect = [
            {'1': {'transactions': transactions}},
            esg_data
        ]
        self.mock_calculations.get_company_env_score.side_effect = lambda t, esg: 85.5

        result = self.use_case.get_data_from_firestore_use_case(user_id)
        expected_transactions = [{'merchant_name': 'Company A', 'esg_score': 85.5}]
        self.assertEqual(result, expected_transactions)
    """

class CalculationTests(unittest.TestCase):
    def setUp(self):
        self.calculations = Calculations()
        self.ESG_scores = {
            'Amazon': {'environment_score': 200},
            'Walmart': {'environment_score': 250},
            'Subway': {'environment_score': 500},
        }

    def test_get_closest_match_above_cutoff(self):
        query = 'Amazon'
        result = self.calculations._get_closest_match(query, self.ESG_scores, score_cutoff=75)
        self.assertEqual(result, 'Amazon')

    def test_get_closest_match_below_cutoff(self):
        query = 'Unknown Company'
        result = self.calculations._get_closest_match(query, self.ESG_scores, score_cutoff=90)
        self.assertIsNone(result)

    def test_get_company_env_score_with_match(self):
        transaction = {'merchant_name': 'Walmart'}
        score = self.calculations.get_company_env_score(transaction, self.ESG_scores)
        self.assertEqual(score, 250)

    def test_get_company_env_score_without_match(self):
        transaction = {'merchant_name': 'RATTM'}
        score = self.calculations.get_company_env_score(transaction, self.ESG_scores)
        self.assertEqual(score, 0)

