from django.urls import path

from . import views

app_name = "suap_login"

urlpatterns = [
    path("erro-tipo-usuario/", views.erro_tipo_usuario, name="erro_tipo_usuario"),
]
