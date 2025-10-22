import random
from collections.abc import Sequence
from typing import Any

import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from factory import Faker
from factory import LazyAttribute
from factory import SubFactory
from factory import post_generation
from factory.django import DjangoModelFactory
from factory.django import ImageField

from sistema_pei.people.constants import EDUCATIONAL_NECESSITIES_CHOICES
from sistema_pei.people.management.commands.load_db_people import Command
from sistema_pei.people.models import AlertaGlobal
from sistema_pei.people.models import Campus
from sistema_pei.people.models import Notification
from sistema_pei.people.models import Responsible
from sistema_pei.people.models import SpecificNecessitie
from sistema_pei.people.models import Student
from sistema_pei.people.models import StudentFile
from sistema_pei.people.models import Teacher
from sistema_pei.users.models import User
from sistema_pei.users.tests.factories import UserFactory


class CampusFactory(DjangoModelFactory):
    """Factory para o modelo Campus usando os campi reais do IFRN."""

    @factory.lazy_attribute
    def name(self):
        """Seleciona um nome de campus real do IFRN."""
        campi = Command().get_campus()
        campus_names = [campus[0] for campus in campi]
        return random.choice(campus_names)  # noqa: S311

    @factory.lazy_attribute
    def abbreviation(self):
        """Retorna a abreviação correspondente ao nome do campus."""
        campi = Command().get_campus()
        campus_dict = dict(campi)
        return campus_dict.get(self.name, "???")

    class Meta:
        model = Campus
        django_get_or_create = ["name"]


class SpecificNecessitieFactory(DjangoModelFactory):
    """Factory para o modelo SpecificNecessitie usando as necessidades educacionais
    reais do IFRN."""

    name = factory.Faker("random_element", elements=EDUCATIONAL_NECESSITIES_CHOICES)

    class Meta:
        model = SpecificNecessitie
        django_get_or_create = ["name"]


class TeacherFactory(DjangoModelFactory):
    """Factory para o modelo Teacher."""

    name = Faker("name", locale="pt_BR")
    email = Faker("email")
    user = SubFactory(UserFactory)
    campus = SubFactory(CampusFactory)

    @factory.lazy_attribute
    def photo(self):
        """Gera foto de perfil realista para o estudante."""
        import random

        gender = random.choice(["men", "women"])  # noqa: S311
        photo_id = random.randint(0, 99)  # noqa: S311
        return f"https://randomuser.me/api/portraits/{gender}/{photo_id}.jpg"

    code = Faker("numerify", text="######")

    class Meta:
        model = Teacher
        django_get_or_create = ["email"]

    @post_generation
    def photoAlt(self, create, extracted, **kwargs):
        """Gera uma imagem alternativa se solicitado."""
        if not create:
            return

        if extracted:
            self.photoAlt = extracted


class ResponsibleFactory(DjangoModelFactory):
    """Factory para o modelo Responsible."""

    name = Faker("name", locale="pt_BR")
    email = Faker("email")

    class Meta:
        model = Responsible
        django_get_or_create = ["email"]


class StudentFactory(DjangoModelFactory):
    """Factory para o modelo Student."""

    name = Faker("name", locale="pt_BR")
    email = Faker("email")
    user = SubFactory(UserFactory)
    registration = Faker("numerify", text="########")

    personal_history = Faker("text", max_nb_chars=500, locale="pt_BR")
    image = ImageField(filename="student.jpg")
    general_necessitie = Faker("text", max_nb_chars=300, locale="pt_BR")
    creation_reasons = Faker("text", max_nb_chars=300, locale="pt_BR")
    abilities = Faker("text", max_nb_chars=300, locale="pt_BR")
    dificulties = Faker("text", max_nb_chars=300, locale="pt_BR")
    specific_necessities = Faker("text", max_nb_chars=300, locale="pt_BR")

    @factory.lazy_attribute
    def course(self):
        """Cria ou obtém um curso dinamicamente para evitar import circular."""
        from sistema_pei.academics.models import Course

        # Tenta pegar um curso existente primeiro
        existing_course = Course.objects.first()
        if existing_course:
            return existing_course

        # Se não existe, importa e cria um novo
        from sistema_pei.academics.tests.factories import CourseFactory

        return CourseFactory.create()

    reference_period = Faker("random_int", min=1, max=8)
    sectors = LazyAttribute(
        lambda obj: [choice[0] for choice in User.Sector.choices[:2]],
    )

    class Meta:
        model = Student
        django_get_or_create = ["registration"]

    @post_generation
    def educational_necessities(self, create, extracted: Sequence[Any], **kwargs):
        """Adiciona necessidades educacionais específicas."""
        if not create:
            return

        if extracted:
            for necessity in extracted:
                self.educational_necessities.add(necessity)
        else:
            # Cria algumas necessidades aleatórias
            num_necessities = random.randint(1, 3)  # noqa: S311
            necessities = SpecificNecessitieFactory.create_batch(num_necessities)
            for necessity in necessities:
                self.educational_necessities.add(necessity)


class StudentFileFactory(DjangoModelFactory):
    """Factory para o modelo StudentFile."""

    student = SubFactory(StudentFactory)
    file = factory.LazyAttribute(
        lambda obj: SimpleUploadedFile(
            "test_file.pdf",
            b"file content",
            content_type="application/pdf",
        ),
    )

    class Meta:
        model = StudentFile


class NotificationFactory(DjangoModelFactory):
    """Factory para o modelo Notification."""

    title = Faker("sentence", nb_words=4, locale="pt_BR")
    text = Faker("text", max_nb_chars=200, locale="pt_BR")
    user = SubFactory(UserFactory)
    viewed = Faker("boolean", chance_of_getting_true=25)
    type = Faker(
        "random_element",
        elements=[choice[0] for choice in Notification.Type.choices],
    )
    action = Faker("url")

    class Meta:
        model = Notification


class AlertaGlobalFactory(DjangoModelFactory):
    """Factory para o modelo AlertaGlobal."""

    mensagem = Faker("text", max_nb_chars=200, locale="pt_BR")
    data_inicio = Faker(
        "date_time_this_month",
        before_now=True,
        tzinfo=timezone.get_current_timezone(),
    )
    data_fim = Faker(
        "date_time_this_month",
        after_now=True,
        tzinfo=timezone.get_current_timezone(),
    )
    cor_base = Faker(
        "random_element",
        elements=[choice[0] for choice in AlertaGlobal.COR_CHOICES],
    )

    class Meta:
        model = AlertaGlobal

    @classmethod
    def create_active(cls, **kwargs):
        """Cria um alerta global ativo (válido no momento atual)."""
        now = timezone.now()
        return cls.create(
            data_inicio=now - timezone.timedelta(days=1),
            data_fim=now + timezone.timedelta(days=1),
            **kwargs,
        )

    @classmethod
    def create_expired(cls, **kwargs):
        """Cria um alerta global expirado."""
        now = timezone.now()
        return cls.create(
            data_inicio=now - timezone.timedelta(days=5),
            data_fim=now - timezone.timedelta(days=1),
            **kwargs,
        )

    @classmethod
    def create_future(cls, **kwargs):
        """Cria um alerta global futuro."""
        now = timezone.now()
        return cls.create(
            data_inicio=now + timezone.timedelta(days=1),
            data_fim=now + timezone.timedelta(days=5),
            **kwargs,
        )
