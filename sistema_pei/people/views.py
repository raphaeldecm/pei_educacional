from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect
from sistema_pei.people.models import User

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
        login(request, user)

        return redirect('/')
    else:
        return render(request, '403.html')
