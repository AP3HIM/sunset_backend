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
        base = os.environ.get("BACKEND_BASE_URL")
        if not base:
            raise ImproperlyConfigured("Missing BACKEND_BASE_URL environment variable")
        base = base.rstrip("/")
        # main urls likely include path("api/", ...), so append /api here:
        return f"{base}/api/accounts/confirm-email/{emailconfirmation.key}/"
