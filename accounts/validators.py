# accounts/validators.py
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class StrongPasswordValidator:
    """
    Enforces at least:
    - One uppercase letter
    - One digit
    - One special character (#, @, $, %, etc.)
    """

    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError(_("Password must contain at least one uppercase letter."))
        if not re.search(r'\d', password):
            raise ValidationError(_("Password must contain at least one digit."))
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=]', password):
            raise ValidationError(_("Password must contain at least one special character."))

    def get_help_text(self):
        return _(
            "Your password must contain at least one uppercase letter, one digit, "
            "and one special character."
        )
