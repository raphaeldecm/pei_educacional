# coding: utf-8

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

from social_core.backends.oauth import BaseOAuth2
from django.contrib.auth.models import Group

class SuapOAuth2(BaseOAuth2):
    name = 'suap'
    AUTHORIZATION_URL = 'https://suap.ifrn.edu.br/o/authorize/'
    ACCESS_TOKEN_METHOD = 'POST'
    ACCESS_TOKEN_URL = 'https://suap.ifrn.edu.br/o/token/'
    ID_KEY = 'identificacao'
    RESPONSE_TYPE = 'code'
    REDIRECT_STATE = True
    STATE_PARAMETER = True
    USER_DATA_URL = 'https://suap.ifrn.edu.br/api/eu/'

    def user_data(self, access_token, *args, **kwargs):
        return self.request(
            url=self.USER_DATA_URL,
            data={'scope': kwargs['response']['scope']},
            method='GET',
            headers={'Authorization': 'Bearer {0}'.format(access_token)}
        ).json()

    def get_user_details(self, response):
        """
        Retorna um dicionário mapeando os fields do settings.AUTH_USER_MODEL.
        você pode fazer aqui outras coisas, como salvar os dados do usuário
        (`response`) em algum outro model.
        """
        splitted_name = response['nome'].split()
        first_name, last_name = splitted_name[0], ''
        if len(splitted_name) > 1:
            last_name = splitted_name[-1]
        return {
            'username': response[self.ID_KEY],
            'first_name': first_name.strip(),
            'last_name': last_name.strip(),
            'email': response['email'],
            'name': response['nome'],
        }
