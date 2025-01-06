# id_validator/helpers.py
import re
from datetime import datetime

def validate_national_id(national_id):
    """
    Validates the national ID format and its date of birth component.
    """
    if not re.match(r'^\d{14}$', national_id):
        return False, "Invalid format: National ID must be 14 digits."
    
    year = int(national_id[1:3])
    month = int(national_id[3:5])
    day = int(national_id[5:7])

    # Determine century based on the first digit
    century = 1900 if national_id[0] == "2" else 2000

    try:
        birth_date = datetime(century + year, month, day)
    except ValueError:
        return False, "Invalid date of birth in National ID."
    
    return True, None

def extract_info(national_id):
    """
    Extracts information like birth year, month, and day from a valid national ID.
    """
    year = int(national_id[1:3])
    month = int(national_id[3:5])
    day = int(national_id[5:7])
    century = 1900 if national_id[0] == "2" else 2000
    birth_year = century + year

    return {
        "birth_year": birth_year,
        "birth_month": month,
        "birth_day": day,
    }
