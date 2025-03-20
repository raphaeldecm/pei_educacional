from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sistema_pei.people.models import Student

from .serializers import EnrollmentUpdateDataSerializer


class EnrollmentDataView(APIView):
    permission_classes = [IsAuthenticated]  # Ainda exigimos autenticação

    def post(self, request, *args, **kwargs):
        # student = request.user  # Agora, request.user será um Student

        # if not isinstance(student, Student):
        #     return Response({"error": "Usuário autenticado não é um estudante"}, status=status.HTTP_403_FORBIDDEN)

        # # Processa os dados enviados
        # serializer = EnrollmentUpdateDataSerializer(data=request.data.get("enrollments", []), many=True, context={"student": student})

        # if serializer.is_valid():
        #     serializer.save()
        #     return Response({"message": "Dados acadêmicos atualizados com sucesso!"}, status=status.HTTP_200_OK)

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
