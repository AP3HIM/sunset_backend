# accounts/urls.py
from django.urls import path, include
from .views import (
    RegisterView,
    ProtectedView,
    user_profile,
    ResendConfirmationView,
    redirect_confirm_email,
    VerifiedEmailTokenView,
    debug_send_mail,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("resend-confirm/", ResendConfirmationView.as_view(), name="resend-confirm"),

    # JWT login (long-lived access token only)
    path("token/", VerifiedEmailTokenView.as_view(), name="token_obtain_pair"),

    # Auth-protected samples
    path("protected/", ProtectedView.as_view(), name="protected"),
    path("profile/", user_profile, name="profile"),

    # Email confirmation
    path("confirm-email/<key>/", redirect_confirm_email, name="account_confirm_email"),
    path("api/confirm-email/<key>/", redirect_confirm_email, name="account_confirm_email_api"),

    # allauth registration endpoints used by dj_rest_auth (keep)
    path("auth/", include("dj_rest_auth.registration.urls")),

    path("debug-send/", debug_send_mail, name="debug_send_mail"),
]
