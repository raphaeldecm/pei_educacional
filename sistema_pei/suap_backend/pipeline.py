from django.core.exceptions import PermissionDenied

def verificar_tipo_usuario(strategy, details, backend, response, *args, **kwargs):
    """
    Verifica o tipo de usuário retornado pelo SUAP e interrompe o processo
    se o tipo de usuário não for 'Aluno'.
    """
    tipo_usuario = response.get('tipo_usuario')

    if tipo_usuario != 'Professor':
        raise PermissionDenied("Acesso negado: você não é um aluno.")
