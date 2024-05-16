from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from sistema_pei.core import constants


# Create your models here.
class Person(models.Model):
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
        return str(self.person)


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
    responsible = models.ForeignKey(
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

    class Meta:
        verbose_name = _("Discente")
        verbose_name_plural = _("Discentes")

    def __str__(self):
        return str(self.person)
