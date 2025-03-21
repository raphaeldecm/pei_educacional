from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from sistema_pei.academics import managers
from sistema_pei.academics.constants import COURSE_TYPE
from sistema_pei.core.constants import SMALL_CHAR_FIELD_NAME_LENGTH
from sistema_pei.core.models import BaseModel
from sistema_pei.people.models import Teacher


# Create your models here.
class Course(BaseModel):
    class CoursePeriod(models.TextChoices):
        MORNING = "MORNING", _("Matutino")
        AFTERNOON = "AFTERNOON", _("Vespertino")
        NIGHT = "NIGHT", _("Noturno")

    class CourseDurationType(models.TextChoices):
        SEMESTER = "SEMESTER", _("Semestral")
        YEAR = "YEAR", _("Anual")

    name = models.CharField(max_length=80, verbose_name=_("Nome"))
    course_type = models.CharField(
        max_length=55,
        choices=COURSE_TYPE,
        verbose_name=_("Tipo"),
    )
    period = models.CharField(
        max_length=15,
        choices=CoursePeriod.choices,
        verbose_name=_("Turno"),
    )

    duration_type = models.CharField(
        choices=CourseDurationType.choices,
        verbose_name=_("Tipo de duração"),
    )

    number_of_periods = models.PositiveSmallIntegerField(
        verbose_name=_("Número de períodos/Anos"),
        validators=[
            MinValueValidator(1),
        ],
    )

    class Meta:
        verbose_name = _("Curso")
        verbose_name_plural = _("Cursos")

    def __str__(self):
        return self.name + " - " + self.get_period_display()


class Subject(BaseModel):
    class SubjectsDuration(models.TextChoices):
        SEMESTER = "SEMESTER", _("Semestral")
        YEAR = "YEAR", _("Anual")

    name = models.CharField(max_length=100)
    subject_type = models.CharField(
        max_length=15,
        choices=SubjectsDuration.choices,
        verbose_name=_("Duração"),
    )
    courses = models.ManyToManyField(
        Course,
        verbose_name=_("Cursos"),
        related_name="subjects",
    )
    objective = models.TextField(
        verbose_name=_("Objetivos"),
        blank=True,
    )
    content = models.TextField(
        verbose_name=_("Conteúdo"),
        blank=True,
    )
    methodology = models.TextField(
        verbose_name=_("Metodologia"),
        blank=True,
    )
    resources = models.TextField(
        verbose_name=("Recursos"),
        blank=True,
    )
    assessments = models.TextField(
        verbose_name=_("Avaliações"),
        blank=True,
    )

    class Meta:
        verbose_name = _("Disciplina")
        verbose_name_plural = _("Disciplinas")

    def __str__(self):
        return self.name


class Offer(BaseModel):
    class OfferStatus(models.TextChoices):
        OPEN = "Aberta", "Aberta"
        CLOSED = "Fechada", "Fechada"

    class Semester(models.IntegerChoices):
        FIRST = 1, _("1º Semestre")
        SECOND = 2, _("2º Semestre")

    status = models.CharField(
        verbose_name=_("Situação"),
        max_length=SMALL_CHAR_FIELD_NAME_LENGTH,
        choices=OfferStatus.choices,
        default=OfferStatus.OPEN,
    )
    subject = models.ForeignKey(
        Subject,
        verbose_name=_("Disciplina"),
        on_delete=models.PROTECT,
        related_name="offers",
    )
    course = models.ForeignKey(
        Course,
        verbose_name=_("Curso"),
        on_delete=models.PROTECT,
        related_name="courses",
    )
    teachers = models.ManyToManyField(
        Teacher,
        verbose_name=_("Professor"),
        related_name="offers",
    )

    year = models.PositiveSmallIntegerField(verbose_name=_("Ano referência do período letivo"))
    semester = models.PositiveSmallIntegerField(
        verbose_name=_("Semestre referência do período letivo"),
        choices=Semester.choices,
    )

    objects = managers.OfferManager()

    class Meta:
        verbose_name = _("Oferta")
        verbose_name_plural = _("Ofertas")

    def student_count(self):
        return self.enrollments.count()

    def __str__(self):
        return self.subject.name


class Enrollment(BaseModel):
    offer = models.ForeignKey(
        Offer,
        verbose_name=_("Oferta"),
        on_delete=models.PROTECT,
        related_name="enrollments",
    )
    student = models.ForeignKey(
        "people.Student",
        verbose_name=_("Aluno"),
        on_delete=models.PROTECT,
    )

    grade1 = models.DecimalField(
        verbose_name=_("1 - Bimestre"),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    absences1 = models.PositiveIntegerField(
        verbose_name=_("Faltas 1 Bimestre"),
        default=0,
    )
    grade2 = models.DecimalField(
        verbose_name=_("2 - Bimestre"),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    absences2 = models.PositiveIntegerField(
        verbose_name=_("Faltas 2 Bimestre"),
        default=0,
    )
    grade3 = models.DecimalField(
        verbose_name=_("3 - Bimestre"),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    absences3 = models.PositiveIntegerField(
        verbose_name=_("Faltas 3 Bimestre"),
        default=0,
    )
    grade4 = models.DecimalField(
        verbose_name=_("4 - Bimestre"),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    absences4 = models.PositiveIntegerField(
        verbose_name=_("Faltas 4 Bimestre"),
        default=0,
    )

    YearSemesterReference = models.IntegerField(_("Cursado no semestre/ano do curso"))

    class Meta:
        unique_together = ("offer", "student")
        verbose_name = _("Inscrição")
        verbose_name_plural = _("Inscrições")

    def calcular_media(self):
        pass

    def __str__(self):
        return f"{self.student} - {self.offer.subject.name}"



class SynchronizationLog(models.Model):
    class Status(models.TextChoices):
        SUCCESS = "SUCCESS", "Sucesso"
        FAILED = "FAILED", "Falha"
        PARTIAL = "PARTIAL", "Parcialmente Completo"
        PENDING = "PENDING", "Pendente"

    student = models.ForeignKey(
        "people.Student",
        verbose_name=_("Discente"),
        on_delete=models.CASCADE,
        related_name="sync_logs",
    )
    sync_date = models.DateTimeField("Data da Sincronização", default=now)
    status = models.CharField(
        "Status",
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    enrollments = models.ManyToManyField(
        Enrollment,
        verbose_name="Matrículas sincronizadas",
        related_name="sync_logs",
        blank=True,
    )
    error_details = models.JSONField("Detalhes dos erros", blank=True, null=True)

    def __str__(self):
        return f"Sync {self.id} - {self.student.registration} - {self.status}"
