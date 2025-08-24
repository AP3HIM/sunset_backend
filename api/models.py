# backend/api/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    uploads_remaining = models.IntegerField(default=1)

    def __str__(self):
        return self.username
