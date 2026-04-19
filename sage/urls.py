from django.urls import path
from . import views

urlpatterns = [
    path("generate/", views.generate_captions, name="sage_generate"),
]