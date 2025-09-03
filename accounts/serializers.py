# accounts/serializers.py
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.account.models import EmailAddress
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
        """
        Create an inactive user and trigger the allauth confirmation email.
        """
        request = self.context.get("request")
        email = validated_data.get("email")

        # Create inactive user
        user = User.objects.create_user(
            is_active=False,
            **validated_data
        )

        try:
            # Ensure EmailAddress is created/linked
            email_address, created = EmailAddress.objects.get_or_create(
                user=user,
                email=email,
                defaults={"verified": False, "primary": True},
            )

            if not created:
                email_address.verified = False
                email_address.primary = True
                email_address.save()

            # Let allauth handle confirmation sending
            setup_user_email(request, user, [])
            get_adapter().send_confirmation_mail(request, user)

            logger.info(f"Confirmation email sent to {email}")

        except Exception as e:
            logger.exception("Failed to send confirmation email")
            from django.conf import settings
            if getattr(settings, "DEBUG", False):
                raise

        return user
