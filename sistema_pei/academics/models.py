from django.db import models
from django.utils.translation import gettext_lazy as _

from sistema_pei.academics.constants import COURSE_TYPE
from sistema_pei.core.models import BaseModel
from sistema_pei.people.models import Student
from sistema_pei.people.models import Teacher
from sistema_pei.core.constants import SMALL_CHAR_FIELD_NAME_LENGTH

# Create your models here.
class Course(BaseModel):
    class CoursePeriod(models.TextChoices):
        MORNING = "MORNING", _("Matutino")
        AFTERNOON = "AFTERNOON", _("Vespertino")
        NIGHT = "NIGHT", _("Noturno")

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

    class Meta:
        verbose_name = _("Curso")
        verbose_name_plural = _("Cursos")

    def __str__(self):
        return self.name + " - " + self.period


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

    class Meta:
        verbose_name = _("Disciplina")
        verbose_name_plural = _("Disciplinas")

    def __str__(self):
        return self.name + " - " + self.course.name

class Offer(BaseModel):
    class OfferStatus(models.TextChoices):
        OPEN = "Aberta", "Aberta"
        CLOSED = "Fechada", "Fechada"

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
    year = models.PositiveSmallIntegerField(verbose_name=_("Ano referência"))
    teacher = models.ForeignKey(
        Teacher,
        verbose_name=_("Professor"),
        on_delete=models.PROTECT,
        related_name="offers",
    )

    class Meta:
        verbose_name = _("Oferta")
        verbose_name_plural = _("Ofertas")

    def __str__(self):
        return self.subject.name + " - " + self.teacher.name


class Enrollment(BaseModel):
    offer = models.ForeignKey(
        Offer,
        verbose_name=_("Oferta"),
        on_delete=models.PROTECT,
        related_name="enrollments",
    )
    student = models.ForeignKey(
        Student,
        verbose_name=_("Aluno"),
        on_delete=models.PROTECT,
        related_name="enrollments",
    )
    grade_1 = models.DecimalField(
        verbose_name=_("Nota 1"),
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
    )
    grade_2 = models.DecimalField(
        verbose_name=_("Nota 2"),
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
    )
    grade_3 = models.DecimalField(
        verbose_name=_("Nota 3"),
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
    )
    grade_4 = models.DecimalField(
        verbose_name=_("Nota 4"),
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ('offer', 'student')
        verbose_name = _("Matrícula")
        verbose_name_plural = _("Matrículas")

    def calcular_media(self):
        notas = [self.nota1, self.nota2, self.nota3, self.nota4]
        notas = [nota for nota in notas if nota is not None]
        return sum(notas) / len(notas) if notas else None

    def __str__(self):
        return f'{self.aluno.nome} - {self.oferta.disciplina.nome} - {self.oferta.ano}'
