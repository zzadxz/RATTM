from django.test import TestCase 
from django.urls import reverse 
from unittest.mock import patch, MagicMock 
from django.http import JsonResponse 
import json 
from map.views import MapView
from map.use_cases import MapUseCase
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

# test views.py and use_case.py 
class ViewsTestCase(TestCase): 
    """
    Test map.view.  
    """
    def setUp(self):
        # the mock data for testing 
        self.user_id = '0'

    @patch('map.use_cases.MapUseCase.get_user_all_locations_and_company')
    def test_map_use_case(self, mock_get_user_all_locations_and_company):
        """
        Test that MapUseCase returns the correct information. 
        """
        user_map = MapUseCase(self.user_id)
        expected_map_data = [{"location": (88.26035, 75.466192), "merchant_name": "Uber", "merchant_percentile": 3}, {"location": (17.020551, -57.127564), "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": (-75.633331, 2.958381), "merchant_name": "Uber", "merchant_percentile": 3}, {"location": (-72.846083, 169.547942), "merchant_name": "Starbucks", "merchant_percentile": 4}, {"location": (-51.878229, -79.332151), "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": (39.796356, 167.669685), "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": (-71.475794, -161.115052), "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": (60.900455, 78.617571), "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": (-62.94921, 175.384574), "merchant_name": "Starbucks", "merchant_percentile": 4}, {"location": (-11.93821, 76.812633), "merchant_name": "Lyft", "merchant_percentile": 3}, {"location": (-38.710865, -11.936035), "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": (3.648657, 8.686896), "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": (25.936513, -58.436286), "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": (-29.749457, 73.136477), "merchant_name": "Uber", "merchant_percentile": 3}, {"location": (5.866038, -118.725815), "merchant_name": "Target", "merchant_percentile": 2}, {"location": (2.174002, 145.897031), "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": (-4.047713, -65.173013), "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": (79.00523, -97.385509), "merchant_name": "Target", "merchant_percentile": 2}, {"location": (-81.345784, 126.140238), "merchant_name": "Uber", "merchant_percentile": 3}, {"location": (22.330367, -71.485464), "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": (-26.476566, -31.799165), "merchant_name": "Lyft", "merchant_percentile": 3}, {"location": (44.783912, 81.293886), "merchant_name": "Uber", "merchant_percentile": 3}, {"location": (71.497947, -6.378674), "merchant_name": "Uber", "merchant_percentile": 3}, {"location": (-65.597454, 88.731136), "merchant_name": "Target", "merchant_percentile": 2}, {"location": (-6.997066, 159.941119), "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": (-34.022381, -47.734434), "merchant_name": "Target", "merchant_percentile": 2}, {"location": (-21.559461, 136.612372), "merchant_name": "Starbucks", "merchant_percentile": 4}, {"location": (32.544367, 101.548583), "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": (55.265151, 45.007168), "merchant_name": "Uber", "merchant_percentile": 3}, {"location": (6.729, -81.175932), "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": (-29.104179, -158.636863), "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": (23.378072, 37.330195), "merchant_name": "Starbucks", "merchant_percentile": 4}, {"location": (-78.179121, 129.175719), "merchant_name": "Uber", "merchant_percentile": 3}, {"location": (-4.102659, 93.199236), "merchant_name": "Starbucks", "merchant_percentile": 4}, {"location": (-87.104728, 163.811977), "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": (42.358936, -122.681122), "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": (80.718744, 150.235162), "merchant_name": "Uber", "merchant_percentile": 3}, {"location": (52.861278, 108.778184), "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": (71.058645, 39.251017), "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": (29.400995, 178.104457), "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": (73.929604, -81.605588), "merchant_name": "Lyft", "merchant_percentile": 3}]
        mock_get_user_all_locations_and_company.return_value = expected_map_data
        actual_map_data = user_map.get_user_all_locations_and_company()
        self.assertEqual(actual_map_data, expected_map_data)    

    @patch("map.views.MapView")
    def test_get_map_data(self, mock_get_map_data):
        """
        Test that get_map_data returns the correct information given a response.
        """
        test_map_view = MapView()
        request = RequestFactory().get('map/get_map_data/')
        request = self.add_session_to_request(request)
        request.session['user_id'] = '0' # adding session in manually 
        response = test_map_view.get_map_data(request)
        self.assertIsInstance(response, JsonResponse)
        expected_map_data = [{"location": [88.26035, 75.466192], "merchant_name": "Uber", "merchant_percentile": 3}, {"location": [17.020551, -57.127564], "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": [-75.633331, 2.958381], "merchant_name": "Uber", "merchant_percentile": 3}, {"location": [-72.846083, 169.547942], "merchant_name": "Starbucks", "merchant_percentile": 4}, {"location": [-51.878229, -79.332151], "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": [39.796356, 167.669685], "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": [-71.475794, -161.115052], "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": [60.900455, 78.617571], "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": [-62.94921, 175.384574], "merchant_name": "Starbucks", "merchant_percentile": 4}, {"location": [-11.93821, 76.812633], "merchant_name": "Lyft", "merchant_percentile": 3}, {"location": [-38.710865, -11.936035], "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": [3.648657, 8.686896], "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": [25.936513, -58.436286], "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": [-29.749457, 73.136477], "merchant_name": "Uber", "merchant_percentile": 3}, {"location": [5.866038, -118.725815], "merchant_name": "Target", "merchant_percentile": 2}, {"location": [2.174002, 145.897031], "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": [-4.047713, -65.173013], "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": [79.00523, -97.385509], "merchant_name": "Target", "merchant_percentile": 2}, {"location": [-81.345784, 126.140238], "merchant_name": "Uber", "merchant_percentile": 3}, {"location": [22.330367, -71.485464], "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": [-26.476566, -31.799165], "merchant_name": "Lyft", "merchant_percentile": 3}, {"location": [44.783912, 81.293886], "merchant_name": "Uber", "merchant_percentile": 3}, {"location": [71.497947, -6.378674], "merchant_name": "Uber", "merchant_percentile": 3}, {"location": [-65.597454, 88.731136], "merchant_name": "Target", "merchant_percentile": 2}, {"location": [-6.997066, 159.941119], "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": [-34.022381, -47.734434], "merchant_name": "Target", "merchant_percentile": 2}, {"location": [-21.559461, 136.612372], "merchant_name": "Starbucks", "merchant_percentile": 4}, {"location": [32.544367, 101.548583], "merchant_name": "McDonalds", "merchant_percentile": 3}, {"location": [55.265151, 45.007168], "merchant_name": "Uber", "merchant_percentile": 3}, {"location": [6.729, -81.175932], "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": [-29.104179, -158.636863], "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": [23.378072, 37.330195], "merchant_name": "Starbucks", "merchant_percentile": 4}, {"location": [-78.179121, 129.175719], "merchant_name": "Uber", "merchant_percentile": 3}, {"location": [-4.102659, 93.199236], "merchant_name": "Starbucks", "merchant_percentile": 4}, {"location": [-87.104728, 163.811977], "merchant_name": "Amazon", "merchant_percentile": 1}, {"location": [42.358936, -122.681122], "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": [80.718744, 150.235162], "merchant_name": "Uber", "merchant_percentile": 3}, {"location": [52.861278, 108.778184], "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": [71.058645, 39.251017], "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": [29.400995, 178.104457], "merchant_name": "Walmart", "merchant_percentile": 4}, {"location": [73.929604, -81.605588], "merchant_name": "Lyft", "merchant_percentile": 3}]
        mock_get_map_data.return_value = expected_map_data
        actual_map_data = json.loads(response.content)
        self.assertEqual(expected_map_data, actual_map_data)

    def add_session_to_request(self, request):
        """
        Adding session to mock request. 
        """
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()
        return request