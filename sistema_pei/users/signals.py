from django.contrib import messages
from django.contrib.auth.signals import user_logged_in
from django.core.exceptions import ValidationError
from django.dispath import receiver
from django.utils.translation import gettext_lazy as _


@receiver(user_logged_in)
def check_user_sector(sender, instance, **kwargs):
    """
    Check if user has a sector.
    """
    if not instance.sector:
        messages.error(
            instance,
            _("User must have a sector."),
            extra_tags="danger",
        )
        raise ValidationError(_("User must have a sector to login."))
