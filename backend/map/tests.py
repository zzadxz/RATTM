from django.test import TestCase 
from django.urls import reverse 
from unittest.mock import patch, mock_open 
from django.http import JsonResponde 
import json 
from map.views import get_map_data
from map.use_cases import MapUseCase

class ViewsTestCase(TestCase): 
    """
    Test map.view.  
    """

    def setUp(self):
        # the mock data for testing 
        self.mock_data = {

        }

    @patch("map.views.get_map_data")
    def test_get_map_data(self, mock_data):
        mock_data.return_value = ()
        
        