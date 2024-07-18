from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from sistema_pei.academics.constants import COURSE_TYPE
from sistema_pei.core.models import BaseModel
from sistema_pei.people.models import Student
from sistema_pei.people.models import Teacher


# Create your models here.
class Courses(BaseModel):
    class CoursePeriod(models.TextChoices):
        MATUTINO = "Matutino", "Matutino"
        VESPERTINO = "Vespertino", "Vespertino"
        NOTURNO = "Noturno", "Noturno"

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

    number_of_periods = models.PositiveSmallIntegerField(
        verbose_name=_("Número de períodos"),
        default=1,
        validators=[
            MinValueValidator(1),
        ]
    )

    class Meta:
        verbose_name = _("Curso")
        verbose_name_plural = _("Cursos")

    def __str__(self):
        return self.name + " - " + self.period


class Subject(BaseModel):
    class SubjectsDuration(models.TextChoices):
        SEMESTRAL = "Semestral", "Semestral"
        ANUAL = "Anual", "Anual"

    name = models.CharField(max_length=100)
    subject_type = models.CharField(
        max_length=15,
        choices=SubjectsDuration.choices,
        verbose_name=_("Períodos"),
    )
    course = models.ForeignKey(
        Courses,
        on_delete=models.PROTECT,
        verbose_name=_("Curso"),
        related_name="subjects",
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        verbose_name=_("Professor"),
        related_name="subjects",
    )
    students = models.ManyToManyField(
        Student,
        verbose_name=_("Alunos"),
        related_name="subjects",
    )
    year = models.PositiveSmallIntegerField(verbose_name=_("Ano referência"))

    class Meta:
        verbose_name = _("Disciplina")
        verbose_name_plural = _("Disciplinas")

    def __str__(self):
        return self.name + " - " + self.course.name

class StudentGrades(BaseModel):
    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        verbose_name=_("Aluno"),
        related_name="grades",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        verbose_name=_("Matéria"),
        related_name="grades",
    )

    def __str__(self):
        return self.student.name + " - " + self.subject.name
    
class StudentGradesSemestral(StudentGrades):
    grade1 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("1 - Bimestre"))
    grade2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("2 - Bimestre"))

    class Meta:
        verbose_name = _("Nota Semestral")
        verbose_name_plural = _("Notas Semestrais")

class StudentGradesAnual(StudentGrades):
    grade1 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("1 - Bimestre"))
    grade2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("2 - Bimestre"))
    grade3 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("3 - Bimestre"))
    grade4 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("4 - Bimestre"))

    class Meta:
        verbose_name = _("Nota Anual")
        verbose_name_plural = _("Notas Anuais")
