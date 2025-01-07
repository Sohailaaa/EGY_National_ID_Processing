# id_validator/models.py
from django.db import models

class APILog(models.Model):
    """
    Model to log API calls for tracking purposes.
    """
    ip_address = models.GenericIPAddressField()
    national_id = models.CharField(max_length=14)
    timestamp = models.DateTimeField(auto_now_add=True)


class EGYNationalIDInfo(models.Model):
    """
    Model to store important data extracted from an Egyptian National ID.
    """
    national_id = models.CharField(max_length=14, unique=True)
    birth_year = models.IntegerField()
    birth_month = models.IntegerField()
    birth_day = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.national_id} - {self.birth_year}-{self.birth_month}-{self.birth_day}"
