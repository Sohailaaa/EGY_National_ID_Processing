# Egyptian National ID Validator API

This project provides an API for validating Egyptian National IDs and extracting relevant information from them, such as birth year, birth month, birth day, and gender. The task also includes rate-limiting, service-to-service authentication using API keys, and logging of all API calls for tracking purposes.

## Features

* **National ID Validation** : The API validates if the provided Egyptian National ID is correct based on format, birth date, and gender information.
* **Data Extraction** : It extracts information such as birth year, month, day, and gender from a valid national ID.
* **Rate Limiting** : API rate-limiting is applied to limit each IP address to 10 requests per minute.
* **API Key Authentication** : The API is secured with API key authentication using `rest_framework_api_key`.
* **Logging** : API calls are logged, including the IP address and national ID, for tracking purposes.
* **Model Persistence** : Valid national IDs and their extracted data are saved to the database for later use.
* **100% Code Coverage** : The application includes unit tests with full code coverage to ensure reliability.

## Getting Started

These instructions will help you set up and run the project locally.

### Prerequisites

* Python 3.8 or higher
* Django 3.2 or higher
* Django REST Framework (DRF)
* PostgreSQL or any other database supported by Django

### Installation

1. clone Repository

   ```
   git clone https://github.com/your-username/egyptian-id-validator.git
   cd egyptian-id-validator

   ```
2. Install dependencies

   ```
   pip install -r requirements.txt

   ```
3. Create a superuser for accessing the Django admin panel
4. ```
   python manage.py createsuperuser

   ```
5. Make your own API key form admin panel
6. Create `.env` file that contains the API key
7. Apply database migrations

   ```
   python manage.py migrate

   ```
8. Run the developmnet server

   ```
   python manage.py runserver

   ```
9. Test the API from `api.http` file that send request or using postman
10. Run the unit testing by running `pytest` in the terminal

### API Endpoints

* **Home Page (GET)** : `http://localhost:8000/`
* Serves the `index.html` template.
* **Validate National ID (POST)** : `http://localhost:8000/api/national-id/`
  * Request :

    ```
    {
      "national_id": "29001011234567"
    }

    ```
  * Response

    ```
    {
      "data": {
        "birth_year": 1990,
        "birth_month": 1,
        "birth_day": 1,
        "gender": "male"
      },
      "message": "Data processed successfully."
    }

    ```

### Testing

1. The project uses `pytest` for testing.

### Code Quality

* **Logging** : We use Python's `logging` module for tracking API calls and validation steps.
* **Environment Configuration** : Configuration is done using `.env` to keep sensitive information out of the codebase.
* **Unit Testing** : Unit tests ensure that the application is robust and functions as expected. Code coverage is 100%.
* **Django Models and Serializers** : We use Django models to store validated national IDs and their extracted information. Serializers ensure that data is formatted correctly before being returned to the client.

### Explanation of Key Files

* **`views.py`** : Contains the API logic for validating and extracting data from the Egyptian National ID. It also handles rate limiting and API key permissions.
* **`models.py`** : Defines the models for logging API calls (`APILog`) and storing validated national ID data (`EGYNationalIDInfo`).
* **`helpers.py`** : Includes the functions to validate the national ID and extract relevant information.
* **`serializers.py`** : Converts data from models to JSON format for the API response.
* **`urls.py`** : Maps the views to URLs.

### Future Enhancements

* **Rate Limiting Configuration** : The rate-limiting logic can be extended to other APIs if needed.
* **API Documentation** : We can integrate tools like Swagger or DRF's built-in documentation to better expose the API to consumers.
* **Error Handling** : The error handling could be improved by adding more detailed exception logging and custom error messages.
* **Advanced Validation** : Add more validation rules, such as checking for duplicate national IDs.

### Conclusion

This project is designed to be an efficient and secure solution for validating Egyptian National IDs and extracting relevant data. It includes modern best practices like rate limiting, API key authentication, logging, and full test coverage to ensure high reliability and maintainability.
