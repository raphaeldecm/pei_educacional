from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from sistema_pei.core import constants
from sistema_pei.core.models import BaseModel
from sistema_pei.core.models import get_sentinel_user

from .constants import EDUCATIONAL_NECESSITIES_CHOICES

User = get_user_model()


# Create your models here.
class Person(BaseModel):
    name = models.CharField(
        verbose_name=_("Nome"),
        max_length=constants.MAX_CHAR_FIELD_NAME_LENGTH,
    )
    email = models.EmailField(
        verbose_name=_("E-mail"),
        max_length=constants.MEDIUM_CHAR_FIELD_NAME_LENGTH,
        unique=True,
    )

    class Meta:
        verbose_name = _("Pessoa")
        verbose_name_plural = _("Pessoas")
        abstract = True

    def __str__(self):
        return self.name


class Teacher(Person):
    class Meta:
        verbose_name = _("Professor")
        verbose_name_plural = _("Professores")

    def __str__(self):
        return self.name


class Responsible(Person):
    class Meta:
        verbose_name = _("Responsável")
        verbose_name_plural = _("Responsáveis")

    def __str__(self):
        return self.name


class SpecificNecessitie(BaseModel):
    name = models.CharField(
        verbose_name=_("Nome"),
        max_length=constants.MAX_CHAR_FIELD_NAME_LENGTH,
        choices=EDUCATIONAL_NECESSITIES_CHOICES,
    )

    class Meta:
        verbose_name = _("Necessidade Específica")
        verbose_name_plural = _("Necessidades Específicas")

    def __str__(self):
        return self.name


class Student(Person):
    class Series(models.IntegerChoices):
        YEAR1 = 1, _("1° Ano")
        YEAR2 = 2, _("2° Ano")
        YEAR3 = 3, _("3° Ano")
        YEAR4 = 4, _("4° Ano")

    serie = models.PositiveSmallIntegerField(
        verbose_name=_("Série"),
        choices=Series.choices,
        validators=[validators.MinValueValidator(1), validators.MaxValueValidator(4)],
    )
    responsible_person = models.ForeignKey(
        Responsible,
        verbose_name=_("Responsável"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="students",
    )
    registration = models.CharField(
        verbose_name=_("Matrícula"),
        max_length=constants.SMALL_CHAR_FIELD_NAME_LENGTH,
        blank=True,
    )
    personal_history = models.TextField(verbose_name=_("Histórico"))
    image = models.ImageField(upload_to="students", verbose_name=_("Foto"))
    general_necessitie = models.TextField(
        verbose_name=_("Outras necessidades educacionais específicas do(a) estudante"),
    )
    creation_reasons = models.TextField(
        verbose_name=_("Motivos para a criação do PEI/ Adaptações"),
    )
    educational_necessities = models.ManyToManyField(
        SpecificNecessitie,
        verbose_name=_("Necessidades Educacionais Específicas"),
    )
    abilities = models.TextField(
        verbose_name=_("Conhecimentos, Habilidades,Capacidades e Interesses"),
    )
    dificulties = models.TextField(verbose_name=_("Dificuldades"))

    specific_necessities = models.TextField(verbose_name=_("Necessidades específicas"))

    class Meta:
        verbose_name = _("Discente")
        verbose_name_plural = _("Discentes")

    def __str__(self):
        return self.name


class Notification(BaseModel):
    class Type(models.TextChoices):
        NEWS = "NEWS", _("News")
        ALERT = "ALERT", _("Alert")
        FAIL = "FAIL", _("Fail")

    title = models.CharField(max_length=255)
    text = models.TextField()
    user = models.ForeignKey(
        User,
        on_delete=get_sentinel_user,
        null=True,
        blank=True,
        related_name="notifications",
    )
    viewed = models.BooleanField(default=False)
    type = models.CharField(
        verbose_name=_("Notification Type"),
        choices=Type.choices,
        max_length=constants.SMALL_CHAR_FIELD_NAME_LENGTH,
    )

    def __str__(self) -> str:
        return super().__str__()
