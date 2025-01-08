# id_validator/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from rest_framework_api_key.permissions import HasAPIKey
from .helpers import validate_national_id, extract_info
from .models import APILog, EGYNationalIDInfo
from .serializers import APILogSerializer, EGYNationalIDInfoSerializer
from django.shortcuts import render


@ratelimit(key='ip', rate='10/m', block=True)
def index(request):
    """
    Renders the index.html template for the homepage.
    Limited to 10 requests per minute per IP address.
    """
    
    return render(request, 'index.html')


class NationalIDValidatorView(APIView):
    """
    API view for validating and extracting information from an Egyptian National ID.
    Limited to 10 requests per minute per IP address.
    """
    permission_classes = [HasAPIKey]

    @method_decorator(ratelimit(key='ip', rate='10/m', block=True))
    def post(self, request):
        national_id = request.data.get("national_id")
      
        is_valid, error_message = validate_national_id(national_id)
        if not is_valid:
            return Response({"error": error_message}, status=400)

        # Extract data
        extracted_data = extract_info(national_id)

        # Log API call
        APILog.objects.create(
            ip_address=request.META.get("REMOTE_ADDR"),
            national_id=national_id,
        )

        # Save extracted data to the model
        egy_info, created = EGYNationalIDInfo.objects.get_or_create(
            national_id=national_id,
            defaults={
                "birth_year": extracted_data["birth_year"],
                "birth_month": extracted_data["birth_month"],
                "birth_day": extracted_data["birth_day"],
            },
        )

        # Serialize and return data
        egy_info_serializer = EGYNationalIDInfoSerializer(egy_info)

        return Response({
            "data": egy_info_serializer.data,
            "message": "Data processed successfully.",
        }, status=200)
