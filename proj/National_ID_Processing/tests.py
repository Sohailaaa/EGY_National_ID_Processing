from django.test import TestCase
from rest_framework.test import APIClient
from .helpers import validate_national_id, extract_info
from rest_framework_api_key.models import APIKey
import unittest
from unittest.mock import Mock
from datetime import datetime

class NationalIDTests(TestCase):
    def setUp(self):
        # Generate an API key for testing
        self.api_key, _ = APIKey.objects.create_key(name="test")
        self.api_key = str(self.api_key)

        # Array of invalid IDs with descriptions
        self.invalid_ids = [
            {"id": "2900101123456", "description": "Invalid length (13 digits)"},
            {"id": "290010112345678", "description": "Invalid length (15 digits)"},
            {"id": "29001011ABCD67", "description": "Non-numeric characters"},
            {"id": "29002301234567", "description": "Invalid date (February 30th)"},
            {"id": "39001301234567", "description": "Future birth year (2090)"},
            {"id": "29022829234567", "description": "Invalid date (February 29th, non-leap year)"},
            {"id": "29013231234567", "description": "Invalid month (13)"},
            {"id": "290010001234567", "description": "Invalid day (day 0)"},
        ]
        
        # Array of valid IDs with descriptions
        self.valid_ids = [
            {"id": "29001011234567", "description": "Valid National ID, male"},
            {"id": "32402222234568", "description": "Valid leap year date (February 29th), female"},
        ]
        
    def test_invalid_ids(self):
        # Manually mock datetime.now() to a fixed date
        mock_datetime = Mock(wraps=datetime)
        mock_datetime.now.return_value = datetime(2025, 1, 7)  # Mocked current date

        for test_case in self.invalid_ids:
            with self.subTest(test_case=test_case):
                national_id = test_case["id"]
                description = test_case["description"]
                is_valid, error_message = validate_national_id(national_id, current_date=mock_datetime.now())
                self.assertFalse(is_valid, f"Failed for {description}: {national_id}")
                self.assertIsNotNone(error_message, f"Error message is missing for {description}")

    def test_valid_ids(self):
        # Manually mock datetime.now() to a fixed date
        mock_datetime = Mock(wraps=datetime)
        mock_datetime.now.return_value = datetime(2025, 1, 7)  # Mocked current date

        for test_case in self.valid_ids:
            with self.subTest(test_case=test_case):
                national_id = test_case["id"]
                description = test_case["description"]
                is_valid, error_message = validate_national_id(national_id, current_date=mock_datetime.now())
                self.assertTrue(is_valid, f"Failed for {description}: {national_id}")
                self.assertIsNone(error_message, f"Unexpected error message for {description}: {national_id}")
                
                # Extract info and validate details for valid IDs
                extracted_info = extract_info(national_id)
                self.assertIn("birth_year", extracted_info, f"Birth year missing for {description}: {national_id}")
                self.assertIn("birth_month", extracted_info, f"Birth month missing for {description}: {national_id}")
                self.assertIn("birth_day", extracted_info, f"Birth day missing for {description}: {national_id}")
                self.assertIn("gender", extracted_info, f"Gender missing for {description}: {national_id}")
    
'''
    def test_api_endpoint(self):
        """
        Test the API endpoint with valid and invalid IDs.
        """
        # Pass the API key in the header for authentication
        self.client.credentials(HTTP_AUTHORIZATION=f"Api-Key {self.api_key}")

        # Valid ID case
        response = self.client.post("/api/national-id/", {"national_id": "29001011234567"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.data)
        self.assertIn("message", response.data)

        # Invalid ID cases
        for case in self.invalid_ids:
            with self.subTest(msg=case["description"], id=case["id"]):
                response = self.client.post("/api/national-id/", {"national_id": case["id"]})
                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.data)

    def test_extract_info_with_valid_ids(self):
        """
        Test extract_info for valid IDs.
        """
        for case in self.valid_ids:
            with self.subTest(msg=case["description"], id=case["id"]):
                result = extract_info(case["id"])
                self.assertIsInstance(result, dict, f"Extract info for ID: {case['id']} should return a dictionary")
                self.assertIn("birth_year", result)
                self.assertIn("birth_month", result)
                self.assertIn("birth_day", result)
                
'''
