from django.contrib.auth import get_user_model
from django.contrib.auth import models
from django.db import models
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from sistema_pei.core import constants
from sistema_pei.core.models import BaseModel
from sistema_pei.core.models import get_sentinel_user
from sistema_pei.users.decorators import profile

from . import utils as users_utils

User = get_user_model()


# Create your models here.
class Campus(BaseModel):
    name = models.CharField(
        verbose_name=_("Nome"),
        max_length=constants.MAX_CHAR_FIELD_NAME_LENGTH,
        unique=True,
    )
    abbreviation = models.CharField(
        verbose_name=_("Abreviação"),
        max_length=4,
        unique=True,
    )

    class Meta:
        verbose_name = _("Campus")
        verbose_name_plural = _("Campi")

    def __str__(self):
        return self.name


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


@profile
class Coordinator(Person):
    campus = models.ForeignKey(
        Campus,
        on_delete=models.SET_NULL,
        verbose_name=_("Campus"),
        null=True,
        related_name="coordinators",
    )
    photo = models.ImageField(
        upload_to="coordinators",
        verbose_name=_("Foto"),
        blank=True,
    )
    code = models.CharField(
        verbose_name=_("Matrícula"),
        max_length=constants.SMALL_CHAR_FIELD_NAME_LENGTH,
        blank=True,
        unique=True,
    )

    class Meta:
        verbose_name = _("Coordenador")
        verbose_name_plural = _("Coordenadores")

    def __str__(self):
        return self.name


@profile
class Assistant(Person):
    campus = models.ForeignKey(
        Campus,
        on_delete=models.SET_NULL,
        verbose_name=_("Campus"),
        null=True,
        related_name="assistants",
    )
    photo = models.ImageField(
        upload_to="assistants",
        verbose_name=_("Foto"),
        blank=True,
    )

    class Meta:
        verbose_name = _("Assistente")
        verbose_name_plural = _("Assistentes")

    def __str__(self):
        return self.name


@profile
class Teacher(Person):
    user = models.OneToOneField(
        User,
        verbose_name=_("Usuário"),
        related_name="teacher",
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
    )
    campus = models.ForeignKey(
        Campus,
        on_delete=models.SET_NULL,
        verbose_name=_("Campus"),
        null=True,
        related_name="teachers",
    )
    photo = models.URLField(
        verbose_name=_("Foto"),
        blank=True,
        max_length=constants.URL_LENGTH,
    )
    code = models.CharField(
        verbose_name=_("Matrícula"),
        max_length=constants.SMALL_CHAR_FIELD_NAME_LENGTH,
        blank=True,
        unique=True,
    )

    class Meta:
        verbose_name = _("Professor")
        verbose_name_plural = _("Professores")

    def __str__(self):
        return self.name

    @transaction.atomic
    def save(self, **kwargs):
        if self.user:
            try:
                group = models.Group.objects.get(name="Teacher")
            except models.Group.DoesNotExist:
                pass
            else:
                self.user.groups.add(group)

            self.user.email = self.email
            self.user.name = self.name
            self.user.save(update_fields=["email", "name"])

        super().save(**kwargs)

    @transaction.atomic
    def delete(self, **kwargs):
        if self.user_id:
            self.user.is_active = False
            self.user.save(update_fields=["is_active"])
        return super().delete(**kwargs)


@profile
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
    )

    class Meta:
        verbose_name = _("Necessidade Específica")
        verbose_name_plural = _("Necessidades Específicas")

    def __str__(self):
        return self.name


class Student(Person):
    registration = models.CharField(
        verbose_name=_("Matrícula"),
        max_length=constants.SMALL_CHAR_FIELD_NAME_LENGTH,
    )

    personal_history = models.TextField(verbose_name=_("Histórico"))

    image = models.ImageField(upload_to="students", verbose_name=_("Foto"))

    general_necessitie = models.TextField(
        verbose_name=_("Outras necessidades educacionais específicas do(a) estudante"),
        blank=True,
    )

    creation_reasons = models.TextField(
        verbose_name=_("Motivos para a criação do PEI/ Adaptações"),
        blank=True,
    )

    educational_necessities = models.ManyToManyField(
        SpecificNecessitie,
        verbose_name=_("Necessidades Educacionais Específicas"),
    )

    abilities = models.TextField(
        verbose_name=_("Conhecimentos, Habilidades,Capacidades e Interesses"),
        blank=True,
    )

    dificulties = models.TextField(
        verbose_name=_("Dificuldades"),
        blank=True,
    )

    specific_necessities = models.TextField(
        verbose_name=_("Necessidades específicas"),
        blank=True,
    )

    course = models.ForeignKey(
        "academics.Course",
        on_delete=models.PROTECT,
        verbose_name=_("Curso"),
        related_name="students",
    )

    reference_period = models.PositiveSmallIntegerField(
        verbose_name=_("Período de Referência"),
    )

    sectors = models.ManyToManyField(
        "users.Sector",
        verbose_name=_("Setores"),
    )

    class Meta:
        verbose_name = _("Discente")
        verbose_name_plural = _("Discentes")

    def __str__(self):
        return self.name


class StudentFile(models.Model):
    student = models.ForeignKey(
        "Student",
        on_delete=models.CASCADE,
        related_name="files",
    )
    file = models.FileField(upload_to="student_files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Anexo")
        verbose_name_plural = _("Anexos")

    def __str__(self):
        return f"Anexo de {self.student.name}"


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
