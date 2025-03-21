from rest_framework import serializers

from sistema_pei.academics.models import Enrollment
from sistema_pei.academics.models import Offer
from sistema_pei.academics.models import Subject
from sistema_pei.academics.models import SynchronizationLog
from sistema_pei.people.models import Student


class GradeSerializer(serializers.Serializer):
    nota = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        allow_null=True,
    )
    faltas = serializers.IntegerField(min_value=0)

class EnrollmentSerializer(serializers.Serializer):
    disciplina = serializers.CharField()
    segundo_semestre = serializers.BooleanField()
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

        # Criar o log de sincronização
        sync_log = SynchronizationLog.objects.create(
            student=student,
            status=SynchronizationLog.Status.PENDING,
        )

        enrollment_list = []  # Lista de matrículas bem-sucedidas
        error_list = []  # Lista de erros


        for enrollment_data in enrollments_data:
            try:
                subject_name = enrollment_data["disciplina"]
                ano = enrollment_data["ano"]
                second_semester = enrollment_data["segundo_semestre"]

                subject, created = Subject.objects.get_or_create(
                    name=subject_name,
                    # Verificar regra "segundo_semestre": false -> SEMESTER, true -> YEAR
                    subject_type=Subject.SubjectsDuration.SEMESTER
                    if not second_semester
                    else Subject.SubjectsDuration.YEAR,
                )
                if student.course:
                    subject.courses.add(student.course)

                semestre = 2 if second_semester else 1
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
                        "YearSemesterReference": ano,
                    },
                )

                enrollment_list.append(enrollment)  # Adiciona à lista de sucesso

            except Exception as e:
                error_list.append({
                    "disciplina": enrollment_data["disciplina"],
                    "ano": enrollment_data["ano"],
                    "erro": str(e),
                })


        sync_log.enrollments.clear()

        # Atualizar log de sincronização
        if enrollment_list:
            sync_log.enrollments.set(enrollment_list)  # Success enrollments

        if error_list:
            sync_log.status = SynchronizationLog.Status.PARTIAL  # Partial error
            sync_log.error_details = error_list  # erros
        else:
            sync_log.status = SynchronizationLog.Status.SUCCESS

        sync_log.save()

        return {
            "message": "Sincronização concluída!",
            "processed": len(enrollment_list),
        }
