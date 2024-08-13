# views.py

from django.shortcuts import render


def erro_tipo_usuario(request):
    return render(request, "suap_backend/erro_tipo_usuario.html")
