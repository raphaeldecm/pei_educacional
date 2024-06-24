from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.urls import reverse

def verificar_tipo_usuario(strategy, details, backend, response, *args, **kwargs):
    """
    Verifica o tipo de usuário retornado pelo SUAP e interrompe o processo
    se o tipo de usuário não for 'Professor'.
    """

    tipo_usuario = response.get('tipo_usuario')
    if tipo_usuario != 'Professor':
        return HttpResponseRedirect(reverse('suap_login:erro_tipo_usuario'))

    return None


def verifica_grupo_usuario(backend, user, response, *args, **kwargs):
    """
    Verifica se o usuário já pertence ao grupo 'Professor'.
    Se não pertencer, adiciona o usuário ao grupo 'Professor'.
    """

    group_name = 'Professor'
    if user and not user.groups.filter(name=group_name).exists():
        professor_group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(professor_group)
