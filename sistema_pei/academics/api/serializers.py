from django.utils.timezone import now
from rest_framework import serializers

from sistema_pei.academics.constants import DEFAULT_SYNC_SUBJECT_DURATION_TYPE
from sistema_pei.academics.models import Enrollment
from sistema_pei.academics.models import Offer
from sistema_pei.academics.models import Subject
from sistema_pei.people.models import Student


class GradeSerializer(serializers.Serializer):
    nota = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        allow_null=True,
    )
    faltas = serializers.IntegerField(min_value=0)


class EnrollmentResponseSerializer(serializers.ModelSerializer):
    student = serializers.CharField(source="student.registration")
    subject = serializers.CharField(source="offer.subject.name")

    class Meta:
        model = Enrollment
        fields = ["student", "subject", "last_synced_at"]


class EnrollmentSerializer(serializers.Serializer):
    disciplina = serializers.CharField()
    ano = serializers.IntegerField()
    nota_etapa_1 = GradeSerializer()
    nota_etapa_2 = GradeSerializer()
    nota_etapa_3 = GradeSerializer()
    nota_etapa_4 = GradeSerializer()


class StudentNotFoundException(serializers.ValidationError):
    default_detail = "Estudante não encontrado."


class StudentEnrollmentSerializer(serializers.Serializer):
    code = serializers.CharField()
    enrollments = EnrollmentSerializer(many=True)

    def create(self, validated_data):
        student_code = validated_data["code"]
        enrollments_data = validated_data["enrollments"]
        student = Student.objects.filter(registration=student_code).first()

        if not student:
            raise StudentNotFoundException

        sync_enroll_list = []
        sync_error_list = []

        # Mapeia string para o tipo de duração do modelo
        duration_map = {
            "semestral": Subject.SubjectsDuration.SEMESTER,
            "anual": Subject.SubjectsDuration.YEAR,
        }
        subject_duration = duration_map.get(
            DEFAULT_SYNC_SUBJECT_DURATION_TYPE.lower(),
            Subject.SubjectsDuration.SEMESTER,
        )

        for enrollment_data in enrollments_data:
            try:
                subject_name = enrollment_data["disciplina"]
                ano = enrollment_data["ano"]

                subject = Subject.objects.filter(name=subject_name).first()
                if not subject:
                    subject = Subject.objects.create(
                        name=subject_name,
                        subject_type=subject_duration,
                    )

                if student.course:
                    subject.courses.add(student.course)

                semestre = 1  # padrão

                offer, offer_created = Offer.objects.get_or_create(
                    subject=subject,
                    course=student.course,
                    year=ano,
                    semester=semestre,
                    defaults={"status": Offer.OfferStatus.OPEN},
                )

                enrollment, _ = Enrollment.objects.update_or_create(
                    student=student,
                    offer=offer,
                    defaults={
                        "grade1": enrollment_data["nota_etapa_1"]["nota"],
                        "absences1": enrollment_data["nota_etapa_1"]["faltas"],
                        "grade2": enrollment_data["nota_etapa_2"]["nota"],
                        "absences2": enrollment_data["nota_etapa_2"]["faltas"],
                        "grade3": enrollment_data["nota_etapa_3"]["nota"],
                        "absences3": enrollment_data["nota_etapa_3"]["faltas"],
                        "grade4": enrollment_data["nota_etapa_4"]["nota"],
                        "absences4": enrollment_data["nota_etapa_4"]["faltas"],
                        "YearSemesterReference": student.reference_period,
                        "last_synced_at": now(),
                    },
                )

                serialized_enrollment = EnrollmentResponseSerializer(enrollment).data
                sync_enroll_list.append(serialized_enrollment)

            except (
                Subject.DoesNotExist,
                Offer.DoesNotExist,
                Enrollment.DoesNotExist,
                KeyError,
                ValueError,
            ) as e:
                sync_error_list.append(
                    {
                        "data": enrollment_data,
                        "error": str(e),
                    },
                )
                continue

        return {
            "message": "Sincronização concluída!",
            "processed": sync_enroll_list,
            "errors": sync_error_list,
        }


class StudentReferencePeriodSerializer(serializers.Serializer):
    code = serializers.CharField()
    reference_period = serializers.IntegerField(min_value=1)

    def create(self, validated_data):
        student_code = validated_data["code"]
        new_reference = validated_data["reference_period"]

        student = Student.objects.filter(registration=student_code).first()

        if not student:
            raise StudentNotFoundException

        student.reference_period = new_reference
        student.save(update_fields=["reference_period"])

        return {
            "message": "Período de referência atualizado com sucesso.",
            "student": student.registration,
            "new_reference_period": student.reference_period,
        }
