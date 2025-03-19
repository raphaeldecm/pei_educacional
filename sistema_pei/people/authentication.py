from people.models import Student
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


class StudentJWTAuthentication(JWTAuthentication):
    """Autenticação JWT baseada na matrícula do estudante."""

    CODE_NOT_FOUND_MSG = "Matrícula não encontrada no token."
    STUDENT_NOT_FOUND_MSG = "Discente não encontrado."

    def authenticate(self, request):
        auth_result = super().authenticate(request)
        if not auth_result:
            return None

        validated_token = auth_result[1]

        # Captura a matrícula do token
        matricula = validated_token.get("matricula", None)
        if not matricula:
            raise AuthenticationFailed(self.CODE_NOT_FOUND_MSG)

        try:
            student = Student.objects.get(matricula=matricula)
        except Student.DoesNotExist:
            raise AuthenticationFailed(self.STUDENT_NOT_FOUND_MSG) from None

        # Retorna o estudante como "usuário autenticado"
        return (student, validated_token)
