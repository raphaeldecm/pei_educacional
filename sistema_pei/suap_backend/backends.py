"""
Informações enviadas pelo SUAP durante o login

{
    'identificacao': string (Númerica),
    'nome_social': string (ou '' caso não tenha),
    'nome_usual': string (Primeiro nome e sobrenome),
    'nome_registro': string (Nome completo),
    'nome': string (Primeiro nome e sobrenome),
    'primeiro_nome': string,
    'ultimo_nome': string,
    'email': string ('@academico.ifrn.edu.br'),
    'email_secundario': string (@gmail.com),
    'email_google_classroom': string (@escolar.ifrn.edu.br),
    'email_academico': string (@academico.ifrn.edu.br),
    'campus': 'PF',
    'foto': Links com foto de perfil,
    'tipo_usuario': 'Aluno' (Professor tem o tipo: 'Servidor (Docente)'),
    'email_preferencial': string (@academico.ifrn.edu.br)
}
"""

import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from social_core.backends.oauth import BaseOAuth2

User = get_user_model()


class SuapOAuth2(BaseOAuth2):
    name = "suap"
    AUTHORIZATION_URL = "https://suap.ifrn.edu.br/o/authorize/"
    ACCESS_TOKEN_METHOD = "POST"
    ACCESS_TOKEN_URL = "https://suap.ifrn.edu.br/o/token/"
    ID_KEY = "identificacao"
    RESPONSE_TYPE = "code"
    REDIRECT_STATE = True
    STATE_PARAMETER = True
    USER_DATA_URL = "https://suap.ifrn.edu.br/api/eu/"

    def user_data(self, access_token, *args, **kwargs):
        return self.request(
            url=self.USER_DATA_URL,
            data={"scope": kwargs["response"]["scope"]},
            method="GET",
            headers={"Authorization": f"Bearer {access_token}"},
        ).json()

    def get_user_details(self, response):
        """
        Retorna um dicionário mapeando os fields do settings.AUTH_USER_MODEL.
        você pode fazer aqui outras coisas, como salvar os dados do usuário
        (`response`) em algum outro model.
        """
        splitted_name = response["nome"].split()
        first_name, last_name = splitted_name[0], ""
        if len(splitted_name) > 1:
            last_name = splitted_name[-1]
        email = response.get("email") or response.get("email_preferencial")
        return {
            "username": response[self.ID_KEY],
            "first_name": first_name.strip(),
            "last_name": last_name.strip(),
            "email": email,
            "name": response["nome"],
        }


class SuapCredentialsBackend(BaseBackend):
    API_BASE_URL = "https://suap.ifrn.edu.br/api"

    def authenticate(self, request, username=None, password=None):
        resp = requests.post(
            f"{self.API_BASE_URL}/token/pair",
            json={"username": username, "password": password},
        )
        if resp.status_code != 200:
            return None

        tokens = resp.json()
        access_token = tokens.get("access")
        refresh_token = tokens.get("refresh")
        if not access_token:
            return None

        profile_resp = requests.get(
            f"{self.API_BASE_URL}/rh/eu/",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if profile_resp.status_code != 200:
            return None

        dados = profile_resp.json()

        full_name = (
            f"{dados.get('primeiro_nome', '')} {dados.get('ultimo_nome', '')}".strip()
        )

        email = (
            dados.get("email")
            or dados.get("email_preferencial")
            or f"{username}@suap.local"
        )

        user, created = User.objects.update_or_create(
            email=email,
            defaults={
                "name": full_name,
            },
        )

        if request:
            request.session["suap_access_token"] = access_token
            request.session["suap_refresh_token"] = refresh_token

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
