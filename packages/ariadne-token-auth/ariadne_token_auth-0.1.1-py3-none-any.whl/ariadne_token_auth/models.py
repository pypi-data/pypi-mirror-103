import binascii
import os

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import utils


class AuthToken(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="auth_token",
        on_delete=models.CASCADE,
        help_text=_("The user that this token was created for."),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text=_("The date and time this token was created at.")
    )
    token_string = models.TextField(
        help_text=_("The token that will be used for login."),
        editable=False,
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.token_string = self.generate_token_string()
        return super(AuthToken, self).save(*args, **kwargs)

    def generate_token_string(self):
        return binascii.hexlify(os.urandom(utils.TOKEN_LENGTH)).decode()

    def __str__(self):
        return f"Token #{self.pk} for {self.user}"
