# id_validator/serializers.py
from rest_framework import serializers
from .models import APILog, EGYNationalIDInfo

class APILogSerializer(serializers.ModelSerializer):
    """
    Serializer to convert APILog model data to JSON format.
    """
    class Meta:
        model = APILog
        fields = ['id', 'ip_address', 'national_id', 'timestamp']


class EGYNationalIDInfoSerializer(serializers.ModelSerializer):
    """
    Serializer to convert EGYNationalIDInfo model data to JSON format.
    """
    class Meta:
        model = EGYNationalIDInfo
        fields = ['national_id', 'birth_year', 'birth_month', 'birth_day', 'created_at']
