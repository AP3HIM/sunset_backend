# accounts/serializers.py
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from allauth.account.utils import send_email_confirmation

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # If you have a custom user, ensure these fields exist (username/email/password)
        fields = ["username", "email", "password"]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        # inactive until email confirm
        user = User.objects.create_user(is_active=False, **validated_data)
        request = self.context.get("request")
        send_email_confirmation(request, user)
        return user
