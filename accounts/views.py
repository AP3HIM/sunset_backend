# accounts/views.py
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from allauth.account.models import EmailAddress
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailConfirmationHMAC

from .serializers import RegisterSerializer
from .jwt import VerifiedEmailTokenSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Check your email to confirm your account."},
            status=status.HTTP_201_CREATED,
        )

class ResendConfirmationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = (request.data.get("email") or "").lower()
        from allauth.account.models import EmailAddress
        try:
            email_addr = EmailAddress.objects.get(email=email)
            get_adapter().send_confirmation_mail(request, email_addr.user)
        except EmailAddress.DoesNotExist:
            pass
        return Response({"detail": "If that email exists, a new confirmation link was sent."})

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Hello, {request.user.username}. You're authenticated!"})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": getattr(user, "username", ""),
        "email": getattr(user, "email", ""),
    })

class VerifiedEmailTokenView(TokenObtainPairView):
    """
    Issues a (long-lived) access token, but only if user.is_active=True.
    The serializer enforces that.
    """
    serializer_class = VerifiedEmailTokenSerializer

def redirect_confirm_email(request, key):
    """
    Link target used in the Brevo email.
    Confirms the email, forces is_active=True, and redirects to frontend login.
    """
    confirmation = EmailConfirmationHMAC.from_key(key)
    if confirmation:
        confirmation.confirm(request)
        user = confirmation.email_address.user
        if not user.is_active:
            user.is_active = True
            user.save(update_fields=["is_active"])

    return redirect("https://sunsetuploader.com/login")

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def debug_send_mail(request):
    to = request.data.get("to")
    if not to:
        return Response({"error": "provide 'to'"}, status=400)
    from django.core.mail import send_mail
    sent = send_mail(
        subject="Sunset SMTP debug",
        message="If you receive this, Brevo SMTP from Render works.",
        from_email=None,  # uses DEFAULT_FROM_EMAIL
        recipient_list=[to],
        fail_silently=False,
    )
    return Response({"sent": sent})
