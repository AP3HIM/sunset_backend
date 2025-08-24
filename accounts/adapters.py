# accounts/adapters.py
import os
from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import ImproperlyConfigured

class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return True

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        user.is_active = False
        if commit:
            user.save()
        return user

    def get_email_confirmation_url(self, request, emailconfirmation):
        backend_base_url = os.environ.get("BACKEND_BASE_URL")
        if not backend_base_url:
            raise ImproperlyConfigured("Missing BACKEND_BASE_URL environment variable")
        return f"{backend_base_url}/api/accounts/confirm-email/{emailconfirmation.key}/"
