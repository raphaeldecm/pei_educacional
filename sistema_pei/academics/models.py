from django.db import models
from django.utils.translation import gettext_lazy as _

from sistema_pei.core.models import BaseModel
from sistema_pei.people.models import Student
from sistema_pei.people.models import Teacher


# Create your models here.
class Courses(BaseModel):
    class CoursePeriod(models.TextChoices):
        MATUTINO = "Matutino", "Matutino"
        VESPERTINO = "Vespertino", "Vespertino"
        NOTURNO = "Noturno", "Noturno"

    class CourseType(models.TextChoices):
        TECNICO_INTEGRADO = "Técnico Integrado Regular", "Técnico Integrado Regular"
        TECNICO_SUBSEQUENTE = "Técnico Subsequente", "Técnico Subsequente"
        CURSO_SUPERIOR = (
            "Curso Superior de Licenciatura",
            "Curso Superior de Licenciatura",
        )
        POS_GRADUACAO = "Pós-Graduação", "Pós-Graduação"
        TECNICO_INTEGRADO_EJA = "Técnico Integrado EJA", "Técnico Integrado EJA"
        CURSO_SUPERIOR_TECNOLOGIA = (
            "Curso Superior de Tecnologia",
            "Curso Superior de Tecnologia",
        )
        ENGENHARIA = "Engenharia", "Engenharia"
        OUTROS = "Outros", "Outros"

    name = models.CharField(max_length=80, verbose_name=_("Nome"))
    course_type = models.CharField(
        max_length=55,
        choices=CourseType.choices,
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
