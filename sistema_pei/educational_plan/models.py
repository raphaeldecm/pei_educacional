from django.db import models
from django.utils.translation import gettext_lazy as _

from sistema_pei.academics.models import Enrollment
from sistema_pei.core.models import BaseModel
from sistema_pei.educational_plan import managers
from sistema_pei.people.models import Teacher


# Create your models here.
class Pei(BaseModel):
    class StatusChoice(models.TextChoices):
        NOT_START = "NOT_START", _("Não iniciado")
        IN_PROGRESS = "IN_PROGRESS", _("Em andamento")
        FEEDBACK = "FEEDBACK", _("Preenchido")
        COMPLETED = "COMPLETED", _("Finalizado")

    enrollment = models.ForeignKey(
        Enrollment,
        verbose_name=_("Inscrição"),
        on_delete=models.PROTECT,
        related_name="peis",
    )

    responsible_teacher = models.ForeignKey(
        Teacher,
        verbose_name=_("Professor Responsável"),
        on_delete=models.PROTECT,
        related_name="Teachers",
    )

    status = models.CharField(
        max_length=30,
        choices=StatusChoice.choices,
        default=StatusChoice.NOT_START,
    )
    objective = models.TextField(
        verbose_name=_("Objetivos"),
        blank=True,
    )
    adapted_objective = models.TextField(
        verbose_name=_("Objetivos Adaptados"),
        blank=True,
    )
    content = models.TextField(
        verbose_name=_("Conteúdo"),
        blank=True,
    )
    adapted_content = models.TextField(
        verbose_name=_("Conteúdo Adaptado"),
        blank=True,
    )
    methodology = models.TextField(
        verbose_name=_("Metodologia"),
        blank=True,
    )
    adapted_methodology = models.TextField(
        verbose_name=_("Metodologia Adaptada"),
        blank=True,
    )
    resources = models.TextField(
        verbose_name=("Recursos"),
        blank=True,
    )
    adapted_resources = models.TextField(
        verbose_name=_("Recursos Adaptados"),
        blank=True,
    )
    assessments = models.TextField(
        verbose_name=_("Avaliações"),
        blank=True,
    )
    adapted_assessments = models.TextField(
        verbose_name=_("Avaliações Adaptadas"),
        blank=True,
    )

    objects = managers.PeiManager()

    academic_opinion_1 = models.TextField(
        verbose_name=_("Parecer do 1º Bimestre"),
        blank=True,
    )
    academic_opinion_2 = models.TextField(
        verbose_name=_("Parecer do 2º Bimestre"),
        blank=True,
    )
    academic_opinion_3 = models.TextField(
        verbose_name=_("Parecer do 3º Bimestre"),
        blank=True,
    )
    academic_opinion_4 = models.TextField(
        verbose_name=_("Parecer do 4º Bimestre"),
        blank=True,
    )
    academic_opinion_final = models.TextField(
        verbose_name=_("Parecer final"),
        blank=True,
    )

    def __str__(self):
        return (
            "PEI -" + self.enrollment.offer.subject.name + self.enrollment.student.name
        )

    def update_status(self):
        if self.pk:
            if self.status == self.StatusChoice.COMPLETED:
                return

            fields_to_check = [
                self.objective,
                self.adapted_objective,
                self.content,
                self.adapted_content,
                self.methodology,
                self.adapted_methodology,
                self.resources,
                self.adapted_resources,
                self.assessments,
                self.adapted_assessments,
            ]

            filled_fields = [field for field in fields_to_check if field]

            if len(filled_fields) == len(fields_to_check):
                self.status = self.StatusChoice.FEEDBACK
            elif len(filled_fields) > 0:
                self.status = self.StatusChoice.IN_PROGRESS
            else:
                self.status = self.StatusChoice.NOT_START

    def save(self, *args, **kwargs):
        self.update_status()
        super().save(*args, **kwargs)


class FeedbackPei(BaseModel):
    feedback = models.TextField(verbose_name=_("Parecer"))
    pei = models.ForeignKey(
        Pei,
        verbose_name=_("PEI"),
        on_delete=models.CASCADE,
        related_name="feedbacks",
    )

    def __str__(self):
        return self.feedback


class Comment(BaseModel):
    text = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    pei = models.ForeignKey(
        Pei,
        on_delete=models.CASCADE,
        verbose_name=_("PEI"),
        related_name="comments",
    )

    def __str__(self):
        return self.text


class Answer(BaseModel):
    text = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(
        Comment,
        verbose_name=_("Resposta"),
        on_delete=models.CASCADE,
        related_name="answers",
    )

    def __str__(self):
        return self.text
