# id_validator/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from .helpers import validate_national_id, extract_info

class NationalIDTests(TestCase):
    def setUp(self):
        # Array of invalid IDs with descriptions
        self.invalid_ids = [
            {"id": "2900101123456", "description": "Invalid length (13 digits)"},
            {"id": "290010112345678", "description": "Invalid length (15 digits)"},
            {"id": "29001011ABCD67", "description": "Non-numeric characters"},
            {"id": "29002301234567", "description": "Invalid date (February 30th)"},
            {"id": "29001301234567", "description": "Future birth year (2090)"},
            {"id": "49001011234567", "description": "Invalid century indicator (4)"},
            {"id": "29022829234567", "description": "Invalid date (February 29th, non-leap year)"},
            {"id": "29002231234567", "description": "Invalid month (13)"},
            {"id": "290010001234567", "description": "Invalid day (day 0)"},
            {"id": "11101011234567", "description": "Invalid prefix (111)"},
        ]
        
        # Array of valid IDs with descriptions
        self.valid_ids = [
            {"id": "29001011234567", "description": "Valid National ID"},
            {"id": "29002929234567", "description": "Valid leap year date (February 29th)"},
        ]

    def test_validate_national_id(self):
        """
        Test validate_national_id with a range of invalid and valid IDs.
        """
        # Valid IDs
        for case in self.valid_ids:
            with self.subTest(msg=case["description"], id=case["id"]):
                is_valid, error_message = validate_national_id(case["id"])
                self.assertTrue(is_valid, f"ID: {case['id']} should be valid")

        # Invalid IDs
        for case in self.invalid_ids:
            with self.subTest(msg=case["description"], id=case["id"]):
                is_valid, error_message = validate_national_id(case["id"])
                self.assertFalse(is_valid, f"ID: {case['id']} should be invalid")

    def test_extract_info(self):
        """
        Test extract_info for valid and invalid IDs.
        """
        # Test valid national ID
        national_id = "29001011234567"
        expected = {"birth_year": 1990, "birth_month": 1, "birth_day": 1}
        self.assertEqual(extract_info(national_id), expected)

        # Test invalid national IDs
        for case in self.invalid_ids:
            with self.subTest(msg=case["description"], id=case["id"]):
                self.assertIsNone(extract_info(case["id"]), f"Extract info for ID: {case['id']} should return None")

    def test_api_endpoint(self):
        """
        Test the API endpoint with valid and invalid IDs.
        """
        client = APIClient()

        # Valid ID case (authentication required)
        response = client.post("/api/national-id/", {"national_id": "29001011234567"})
        self.assertEqual(response.status_code, 401)  # Requires authentication

        # Invalid ID cases
        for case in self.invalid_ids:
            with self.subTest(msg=case["description"], id=case["id"]):
                response = client.post("/api/national-id/", {"national_id": case["id"]})
                self.assertEqual(response.status_code, 401, "Authentication required")

        # Valid ID cases (authentication required)
        for case in self.valid_ids:
            with self.subTest(msg=case["description"], id=case["id"]):
                response = client.post("/api/national-id/", {"national_id": case["id"]})
                self.assertEqual(response.status_code, 401, "Authentication required")

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
