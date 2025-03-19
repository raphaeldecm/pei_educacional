from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sistema_pei.people.models import Student

from .serializers import EnrollmentUpdateDataSerializer


class EnrollmentDataView(APIView):
    permission_classes = [AllowAny]
    serializer_class = EnrollmentUpdateDataSerializer

    def post(self, request):

        pass
