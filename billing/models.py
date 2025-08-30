from django.db import models
from django.conf import settings

# Create your models here.
# billing/models.py

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=100)

class Subscription(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=100)
    status = models.CharField(max_length=50)  # active, canceled, etc.
    created = models.DateTimeField(auto_now_add=True)
