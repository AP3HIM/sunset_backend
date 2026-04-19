# backend/api/urls.py
from django.urls import path
from .views import create_upload_url

urlpatterns = [ path("r2/upload-url/", create_upload_url, name="r2_upload_url") ]
