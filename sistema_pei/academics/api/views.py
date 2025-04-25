from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sistema_pei.academics.models import Enrollment
from sistema_pei.academics.models import Offer
from sistema_pei.academics.models import Subject
from sistema_pei.people.models import Student

from .serializers import StudentEnrollmentSerializer


class EnrollmentDataView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentEnrollmentSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request, *args, **kwargs):
    #     student = get_object_or_404(Student, registration=request.data.get("code"))
    #     serializer = EnrollmentUpdateDataSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     for enrollment_data in serializer.validated_data["enrollments"]:
    #         subject_name = enrollment_data["disciplina"]
    #         year = enrollment_data["ano"]
    #         second_semester = enrollment_data["segundo_semestre"]

    #         subject, created = Subject.objects.get_or_create(
    #             name=subject_name,
    #              # Verificar regra "segundo_semestre": false -> SEMESTER, true -> YEAR
    #             subject_type=Subject.SubjectsDuration.SEMESTER
    #             if not second_semester
    #             else Subject.SubjectsDuration.YEAR,
    #             course=student.course,
    #         )

    #         offer, created = Offer.objects.get_or_create(
    #             subject=subject,
    #             course=student.course,
    #             year=year,
    #             semester=Offer.Semester.SECOND
    #                 if second_semester
    #                 else Offer.Semester.FIRST,
    #         )

    #         enrollment, created = Enrollment.objects.get_or_create(
    #             student=student,
    #             offer=offer,
    #             YearSemesterReference=year,
    #         )

    #         enrollment.nota_etapa_1 = enrollment_data["nota_etapa_1"]["nota"]
    #         enrollment.faltas_etapa_1 = enrollment_data["nota_etapa_1"]["faltas"]
    #         enrollment.nota_etapa_2 = enrollment_data["nota_etapa_2"]["nota"]
    #         enrollment.faltas_etapa_2 = enrollment_data["nota_etapa_2"]["faltas"]
    #         enrollment.nota_etapa_3 = enrollment_data["nota_etapa_3"]["nota"]
    #         enrollment.faltas_etapa_3 = enrollment_data["nota_etapa_3"]["faltas"]
    #         enrollment.nota_etapa_4 = enrollment_data["nota_etapa_4"]["nota"]
    #         enrollment.faltas_etapa_4 = enrollment_data["nota_etapa_4"]["faltas"]

    #         enrollment.save()

    #     return Response(
    #         {"detail": "Enrollment data updated successfully"},
    #         status=status.HTTP_200_OK,
    #     )
