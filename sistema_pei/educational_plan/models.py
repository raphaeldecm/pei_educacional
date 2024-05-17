from django.db import models
from django.utils.translation import gettext_lazy as _

from sistema_pei.academics.models import Subject
from sistema_pei.core.models import BaseModel
from sistema_pei.people.models import Student


# Create your models here.
class Pei(BaseModel):
    class StatusChoice(models.TextChoices):
        NOT_START = "NOT_START", "Não iniciado"
        IN_PROGRESS = "IN_PROGRESS", "Em andamento"
        COMPLETED = "COMPLETED", "Preenchidos"
        FEEDBACK = "FEEDBACK", "Com parecer"

    subject = models.ForeignKey(
        Subject,
        verbose_name=_("Matéria"),
        on_delete=models.CASCADE,
        related_name="peis",
    )
    student = models.ForeignKey(
        Student,
        verbose_name=_("Aluno"),
        on_delete=models.CASCADE,
        related_name="peis",
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

    def __str__(self):
        return (
            "("
            + self.student.registration
            + ")"
            + self.student.name
            + " / "
            + self.subject.name
        )


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
