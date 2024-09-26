from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse

from sistema_pei.people.models import Campus
from sistema_pei.people.models import Teacher


def verificar_tipo_usuario(strategy, details, backend, response, *args, **kwargs):
    """
    Verifica o tipo de usuário retornado pelo SUAP e interrompe o processo
    se o tipo de usuário não for 'Servidor (Docente)' e o campus não for 'PF'.
    """

    tipo_usuario = response.get("tipo_usuario")
    campus = response.get("campus")

    if tipo_usuario != "Servidor (Docente)" or campus != "PF":
        return HttpResponseRedirect(reverse("suap_login:erro_tipo_usuario"))

    return None


def record_teacher_data(backend, user, response, *args, **kwargs):
    """
    Verifica se o usuário já pertence ao grupo 'Teacher'.
    Se não pertencer, adiciona o usuário ao grupo 'Teacher'.
    """
    try:
        group = Group.objects.get(name="Teacher")
    except Group.DoesNotExist:
        pass
    else:
        user.groups.add(group)
        user.sector = "DIAC"
        user.save(
            update_fields=["is_active", "sector"],
        )

    teacher, created = Teacher.objects.get_or_create(
        code=response.get("identificacao"),
        defaults={
            "user": user,
            "name": response.get("nome"),
            "email": response.get("email_preferencial"),
            "campus": Campus.objects.get(abbreviation=response.get("campus")),
            "code": response.get("identificacao"),
            "photo": response.get("foto"),
        },
    )
    # Associar o User ao Teacher
    if created or not teacher.user:
        teacher.user = user
        teacher.save()
