# accounts/serializers.py
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from allauth.account.utils import setup_user_email
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress, EmailConfirmationHMAC
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(is_active=False, **validated_data)
        request = self.context.get("request")

        try:
            # 1️ Ensure EmailAddress exists
            setup_user_email(request, user, [user.email])

            # 2️ Grab the primary EmailAddress object
            email_address = EmailAddress.objects.get(user=user, email=user.email)
            

            # 3️ Create EmailConfirmation object
            confirmation = EmailConfirmationHMAC(email_address)

            # 4 Send confirmation via adapter
            get_adapter(request).send_confirmation_mail(request, confirmation, signup=True)
            logger.info(f"Confirm URL: {get_adapter(request).get_email_confirmation_url(request, confirmation)}")

            logger.info(f"[accounts] Sent confirmation email to {user.email}")
        except Exception as e:
            logger.exception(f"[accounts] Failed to send confirmation email: {e}")
            from django.conf import settings
            if getattr(settings, "DEBUG", False):
                raise

        return user
