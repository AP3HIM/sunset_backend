# accounts/serializers.py
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from allauth.account.adapter import get_adapter

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
        # Create inactive user until email confirmation
        user = User.objects.create_user(is_active=False, **validated_data)
        request = self.context.get("request")
        try:
            get_adapter().send_confirmation_mail(request, user)
        except Exception as e:
            print(f"Email confirmation failed: {e}")
        return user
