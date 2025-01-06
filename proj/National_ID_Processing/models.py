# id_validator/models.py
from django.db import models

class APILog(models.Model):
    ip_address = models.GenericIPAddressField()
    national_id = models.CharField(max_length=14)
    timestamp = models.DateTimeField(auto_now_add=True)
