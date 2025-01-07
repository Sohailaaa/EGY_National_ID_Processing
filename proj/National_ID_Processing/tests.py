from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import Mock
from datetime import datetime
from rest_framework_api_key.models import APIKey
from .helpers import validate_national_id, extract_info

class NationalIDTests(TestCase):
    def setUp(self):
        # Generate an API key for testing
        self.api_key, _ = APIKey.objects.create_key(name="test")
        self.api_key = str(self.api_key)

        # Test data: Invalid IDs
        self.invalid_ids = [
            {"id": "2900101123456", "description": "Invalid length (13 digits)"},
            {"id": "290010112345678", "description": "Invalid length (15 digits)"},
            {"id": "29001011ABCD67", "description": "Non-numeric characters"},
            {"id": "29002301234567", "description": "Invalid date (February 30th)"},
            {"id": "39001301234567", "description": "Future birth year (2090)"},
            {"id": "29002290123456", "description": "Invalid date (February 29th, non-leap year)"},
            {"id": "29013231234567", "description": "Invalid month (13)"},
            {"id": "29001000123456", "description": "Invalid day (day 0)"},
            {"id": "49001000123456", "description": "Invalid century"},


        ]

        # Test data: Valid IDs
        self.valid_ids = [
            {"id": "29001011234567", "description": "Valid National ID, male"},
            {"id": "32402222234568", "description": "Valid leap year date (February 29th), female"},
        ]

    def test_invalid_ids(self):
        """Test invalid IDs using `validate_national_id`."""
        mock_datetime = Mock(wraps=datetime)
        mock_datetime.now.return_value = datetime(2025, 1, 7)

        for test_case in self.invalid_ids:
            with self.subTest(test_case=test_case):
                is_valid, error_message = validate_national_id(test_case["id"], current_date=mock_datetime.now())
                self.assertFalse(is_valid, f"Failed for {test_case['description']}: {test_case['id']}")
                self.assertIsNotNone(error_message, f"Error message is missing for {test_case['description']}")

    def test_valid_ids(self):
        """Test valid IDs using `validate_national_id` and `extract_info`."""
        mock_datetime = Mock(wraps=datetime)
        mock_datetime.now.return_value = datetime(2025, 1, 7)

        for test_case in self.valid_ids:
            with self.subTest(test_case=test_case):
                is_valid, error_message = validate_national_id(test_case["id"])
                self.assertTrue(is_valid, f"Failed for {test_case['description']}: {test_case['id']}")
                self.assertIsNone(error_message, f"Unexpected error message for {test_case['description']}")

                extracted_info = extract_info(test_case["id"])
                self.assertIn("birth_year", extracted_info, f"Birth year missing for {test_case['description']}")
                self.assertIn("birth_month", extracted_info, f"Birth month missing for {test_case['description']}")
                self.assertIn("birth_day", extracted_info, f"Birth day missing for {test_case['description']}")
                self.assertIn("gender", extracted_info, f"Gender missing for {test_case['description']}")

def test_api_endpoint(self):
    """Test the National ID API endpoint."""
    client = APIClient()

    # Set the headers with the API key
    headers = {"HTTP_AUTHORIZATION": f"Api-Key {self.api_key}"}
    
    # Debugging: Print API key to ensure it's correctly set
    print(f"API Key used: {self.api_key}")

    # Test valid ID
    response = client.post("/api/national-id/", {"national_id": self.valid_ids[0]["id"]}, **headers)
    print(response.status_code)  # Debugging: Check the response status code
    self.assertEqual(response.status_code, 200)
    self.assertIn("data", response.data)
    self.assertIn("message", response.data)

    # Test invalid IDs
    for case in self.invalid_ids:
        with self.subTest(test_case=case):
            response = client.post("/api/national-id/", {"national_id": case["id"]}, **headers)
            print(response.status_code)  # Debugging: Check the response status code
            self.assertEqual(response.status_code, 400)
            self.assertIn("error", response.data)


    def test_extract_info_with_valid_ids(self):
        """Test `extract_info` for valid IDs."""
        for case in self.valid_ids:
            with self.subTest(test_case=case):
                result = extract_info(case["id"])
                self.assertIsInstance(result, dict, f"Extract info for {case['id']} should return a dictionary")
                self.assertIn("birth_year", result)
                self.assertIn("birth_month", result)
                self.assertIn("birth_day", result)
                self.assertIn("gender", result)
