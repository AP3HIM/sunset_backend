import logging
from django.db import transaction
from allauth.account.signals import email_confirmed
from django.dispatch import receiver

logger = logging.getLogger(__name__)

@receiver(email_confirmed)
def activate_user_after_email_confirmation(request, email_address, **kwargs):
    with transaction.atomic():
        user = email_address.user
        user.refresh_from_db()
        email_address.refresh_from_db()

        if not user.is_active:
            user.is_active = True
            user.save(update_fields=["is_active"])
