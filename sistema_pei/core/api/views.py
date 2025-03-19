import requests
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from sistema_pei.core.constants import STATUS_CODE_OK
from sistema_pei.core.constants import SUAP_VALIDATION_URL
from sistema_pei.people.models import Student

from .serializers import SUAPTokenSerializer


class SuapTokenValidateView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SUAPTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        suap_jwt = serializer.validated_data["token"]
        suap_code = serializer.validated_data["code"]

        if not Student.objects.filter(registration=suap_code).exists():
            return Response({"error": "Discente não encontrado no sistema pei. "
                             "Entre em contato com o setor responsável"}, status=404)

        verify_response = requests.post(
            SUAP_VALIDATION_URL,
            json={"token": suap_jwt},
            timeout=5,
        )

        if verify_response.status_code != STATUS_CODE_OK:
            return Response({"error": "Token inválido ou expirado"}, status=401)

        refresh = RefreshToken()
        refresh["suap_code"] = suap_code

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })
