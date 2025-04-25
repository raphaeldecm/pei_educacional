# views.py

from django.shortcuts import render


def erro_tipo_usuario(request):
    return render(request, "erro_tipo_usuario.html")
