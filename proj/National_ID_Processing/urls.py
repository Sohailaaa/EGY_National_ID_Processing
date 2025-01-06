# id_validator/urls.py
from django.urls import path
from .views import index, NationalIDValidatorView

urlpatterns = [
    path("", index, name="index"),  # Serve the index.html template on the homepage
    path("api/national-id/", NationalIDValidatorView.as_view(), name="national_id_api"),
]
