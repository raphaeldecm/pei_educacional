from allauth.account.signals import user_logged_in
from django.contrib import messages
from django.contrib.auth import logout
from django.dispatch import receiver
from django.shortcuts import redirect


@receiver(user_logged_in)
def check_user_group(sender, request, user, **kwargs):

    if not user.groups.exists():
        logout(request)
        messages.error(
            request,
            "Você não pertence ao grupo necessário para acessar o sistema.",
        )
        return redirect("account_login")
    return None
