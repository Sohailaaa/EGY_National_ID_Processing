# id_validator/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework_api_key.permissions import HasAPIKey
from .helpers import validate_national_id, extract_info
from .models import APILog
from django.shortcuts import render

def index(request):
    """
    Renders the index.html template for the homepage.
    """
    return render(request, 'index.html')



class NationalIDValidatorView(APIView):
    permission_classes = [HasAPIKey]
    throttle_classes = [UserRateThrottle]  # Rate limiting for API usage

    def post(self, request):
        national_id = request.data.get("national_id")
        if not national_id:
            return Response({"error": "National ID is required."}, status=400)

        is_valid, error_message = validate_national_id(national_id)
        if not is_valid:
            return Response({"error": error_message}, status=400)
        
        # Extract and log data
        extracted_data = extract_info(national_id)
        APILog.objects.create(
            ip_address=request.META.get("REMOTE_ADDR"),
            national_id=national_id,
        )
        return Response({"data": extracted_data}, status=200)
