import re
from datetime import datetime

def is_leap_year(year):
    """Returns True if the year is a leap year."""
    return (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))

def validate_national_id(national_id, current_date=None):
    """
    Validates the national ID format and its date of birth component.
    """
    print(f"Validating National ID: {national_id}")  # Print the ID being validated

    if current_date is None:
        current_date = datetime.now()

    # Check if the ID is exactly 14 digits
    if not re.match(r'^\d{14}$', national_id):
        print("Invalid format: National ID must be 14 digits.")
        return False, "Invalid format: National ID must be 14 digits."

    # Check if the first digit is either 2 or 3
    if national_id[0] not in ['2', '3']:
        print("Invalid first digit in National ID. It must be 2 or 3.")
        return False, "Invalid first digit in National ID. It must be 2 or 3."

    # Extract components from the ID
    birth_year = int(national_id[1:3])  # YY
    month = int(national_id[3:5])  # MM
    day = int(national_id[5:7])    # DD
    gender_digit = int(national_id[12])  # 13th digit (odd for male, even for female)

    # Adjust the birth year based on the first digit
    if national_id[0] == '2':  # Born in the 1990s
        full_birth_year = 1900 + birth_year
    elif national_id[0] == '3':  # Born in the 2000s
        full_birth_year = 2000 + birth_year
  
    # Validate month (1 to 12)
    if month < 1 or month > 12:
        print("Invalid month in National ID.")
        return False, "Invalid month in National ID."

    # Validate day (1 to 31) and handle month-specific days
    if day < 1 or (month == 2 and day > 29) or (month in [4, 6, 9, 11] and day > 30) or (month not in [2, 4, 6, 9, 11] and day > 31):
        print("Invalid day in National ID.")
        return False, "Invalid day in National ID."

    # Handle leap year for February 29
    if month == 2 and day == 29:
        if not is_leap_year(full_birth_year):  # Check leap year based on full birth year
            print("Invalid day in National ID (February 29 on a non-leap year).")
            return False, "Invalid day in National ID (February 29 on a non-leap year)."

    # Validate gender (odd for male, even for female)
    gender = "female" if gender_digit % 2 == 0 else "male"
    print(f"Gender: {gender}")

    # Validate if the year is in the future
    birth_date = datetime(full_birth_year, month, day)
    if birth_date > current_date:
        print(f"Invalid year: Birth year is in the future. Birth Date: {birth_date}, Current Date: {current_date}")
        return False, "Invalid year: Birth year is in the future."

    print("National ID is valid.")
    return True, None
  
def extract_info(national_id):
    """
    Extracts information like birth year, month, day, and gender from a valid national ID.
    """

    # Extract components
    birth_year = int(national_id[1:3])  # YY
    month = int(national_id[3:5])  # MM
    day = int(national_id[5:7])    # DD

    # Adjust the birth year based on the first digit
    if national_id[0] == '2':  # Born in the 1990s
        full_birth_year = 1900 + birth_year
    elif national_id[0] == '3':  # Born in the 2000s
        full_birth_year = 2000 + birth_year
  
    # Determine gender based on the 13th digit (odd for male, even for female)
    gender_digit = int(national_id[12])
    gender = "female" if gender_digit % 2 == 0 else "male"

    # Return extracted info as a dictionary
    return {
        "birth_year": full_birth_year,
        "birth_month": month,
        "birth_day": day,
        "gender": gender
    }
