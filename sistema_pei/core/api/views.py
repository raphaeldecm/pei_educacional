import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from sistema_pei.people.models import Student

from .serializers import SUAPTokenSerializer

SUAP_VALIDATION_URL = "https://suap.ifrn.edu.br/api/eu/"

class SuapTokenValidateView(APIView):
    """Autentica aluno com JWT do SUAP e gera um token JWT próprio baseado no modelo Student."""
    serializer_class = SUAPTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)  # Valida os dados recebidos
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        suap_jwt = serializer.validated_data["suap_token"]

        # Validar o token no SUAP
        headers = {"Authorization": f"Bearer {suap_jwt}"}
        response = requests.get(SUAP_VALIDATION_URL, headers=headers)

        if response.status_code != 200:
            return Response({"error": "Token inválido ou expirado"}, status=401)

        # Extrair os dados do aluno do SUAP
        user_data = response.json()
        registration = user_data.get("matricula")  # Matrícula do aluno (chave única)

        # Buscar aluno no banco de dados
        try:
            student = Student.objects.get(registration=registration)
        except Student.DoesNotExist:
            return Response({"error": "Aluno não encontrado no sistema"}, status=404)

        # Criar um JWT baseado no aluno (sem User)
        refresh = RefreshToken()
        refresh["student_id"] = student.id
        refresh["registration"] = student.registration

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })
