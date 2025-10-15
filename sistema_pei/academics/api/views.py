from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import StudentEnrollmentSerializer
from .serializers import StudentReferencePeriodSerializer


class StudentReferencePeriodView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentReferencePeriodSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnrollmentDataView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentEnrollmentSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
