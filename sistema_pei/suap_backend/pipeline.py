from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse

from sistema_pei.people.models import Campus
from sistema_pei.people.models import Teacher


def verificar_tipo_usuario(strategy, details, backend, response, *args, **kwargs):
    """
    Verifica o tipo de usuário retornado pelo SUAP e interrompe o processo
    se o tipo de usuário não for 'Docente', 'Técnico-Administrativo' ou
    'Prestador de Serviço'.
    """
    tipo_usuario = response.get("tipo_usuario")

    if tipo_usuario not in [
        "Servidor (Docente)",
        "Prestador de Serviço",
        "Servidor (Técnico-Administrativo)",
    ]:
        return HttpResponseRedirect(reverse("suap_login:erro_tipo_usuario"))

    return None


def record_user_data(backend, user, response, *args, **kwargs):
    """
    Verifica o tipo de usuário e chama a função específica para registrar os dados.
    """
    tipo_usuario = response.get("tipo_usuario")

    try:
        collaborator_group = Group.objects.get(name="Collaborator")
        teacher_group = Group.objects.get(name="Teacher")
    except Group.DoesNotExist:
        pass
    else:
        if tipo_usuario == "Servidor (Docente)":
            user.groups.add(teacher_group)
            user.sector = "DIAC"
            user.photo = response.get("foto")
            user.save(
                update_fields=["is_active", "sector", "photo"],
            )
            process_teacher(user, response)
        else:
            if not user.groups.exists():
                user.groups.add(collaborator_group)

            user.sector = "NAPNE"
            user.photo = response.get("foto") or ""
            user.is_active = True
            user.save(
                update_fields=["is_active", "sector", "photo"],
            )


def process_teacher(user, response):
    # Lógica para Docente

    teacher, created = Teacher.objects.get_or_create(
        code=response.get("identificacao"),
        defaults={
            "user": user,
            "name": response.get("nome"),
            "email": response.get("email") or response.get("email_preferencial"),
            "campus": Campus.objects.get(abbreviation=response.get("campus")),
            "code": response.get("identificacao"),
            "photo": response.get("foto"),
        },
    )

    # Atualiza os dados do professor se necessário
    if not created:
        update_teacher_data(teacher, response)

    # Associar o User ao Teacher
    if created or not teacher.user:
        teacher.user = user
        teacher.save()


def update_teacher_data(teacher, response):
    """
    Atualiza os dados do professor.
    """
    teacher.name = response.get("nome")
    teacher.email = response.get("email") or response.get("email_preferencial")
    teacher.campus = Campus.objects.get(abbreviation=response.get("campus"))
    teacher.code = response.get("identificacao")
    teacher.photo = response.get("foto")

    teacher.save(update_fields=["name", "email", "campus", "photo"])
