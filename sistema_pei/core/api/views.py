import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from sistema_pei.core.constants import STATUS_CODE_OK
from sistema_pei.core.constants import SUAP_VALIDATION_URL
from sistema_pei.people.models import Student

from .serializers import SUAPTokenSerializer

User = get_user_model()


class SuapTokenValidateView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SUAPTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        suap_jwt = serializer.validated_data["token"]
        suap_code = serializer.validated_data["code"]

        student = Student.objects.filter(registration=suap_code).first()
        if not student:
            return Response(
                {
                    "error": "Discente não encontrado no sistema pei. "
                    "Entre em contato com o setor responsável",
                },
                status=404,
            )

        verify_response = requests.post(
            SUAP_VALIDATION_URL,
            json={"token": suap_jwt},
            timeout=5,
        )

        if verify_response.status_code != STATUS_CODE_OK:
            return Response({"error": "Token inválido ou expirado"}, status=401)

        # Criar usuário para estudante, se não existir
        user, created = User.objects.get_or_create(
            email=student.email,
            defaults={
                "name": student.name,
                "is_active": True,
            },
        )

        if created:
            user.set_unusable_password()
            user.save()

        student_group, group_created = Group.objects.get_or_create(name="Student")
        user.groups.add(student_group)

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
        )
