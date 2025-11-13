import factory
from django.utils import timezone

from sistema_pei.academics.constants import COURSE_TYPE
from sistema_pei.academics.models import Course
from sistema_pei.academics.models import Enrollment
from sistema_pei.academics.models import Matrix
from sistema_pei.academics.models import Offer
from sistema_pei.academics.models import Subject
from sistema_pei.people.tests.factories import StudentFactory
from sistema_pei.people.tests.factories import TeacherFactory
from sistema_pei.users.tests.factories import UserFactory


class CourseFactory(factory.django.DjangoModelFactory):
    """Factory para o modelo Course."""

    class Meta:
        model = Course

    name = factory.Faker("sentence", nb_words=3, locale="pt_BR")
    course_type = factory.Faker(
        "random_element",
        elements=[choice[0] for choice in COURSE_TYPE],
    )
    period = factory.Faker(
        "random_element",
        elements=[choice[0] for choice in Course.CoursePeriod.choices],
    )
    duration_type = factory.Faker(
        "random_element",
        elements=[choice[0] for choice in Course.CourseDurationType.choices],
    )
    number_of_periods = factory.Faker("random_int", min=2, max=10)
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.SubFactory(UserFactory)


class MatrixFactory(factory.django.DjangoModelFactory):
    """Factory para o modelo Matrix."""

    class Meta:
        model = Matrix

    code = factory.Sequence(lambda n: n + 1000)  # Códigos únicos começando em 1000
    description = factory.Faker("sentence", nb_words=5, locale="pt_BR")
    year = factory.Faker("random_int", min=2015, max=2030)
    active = factory.Faker("boolean", chance_of_getting_true=80)
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.SubFactory(UserFactory)


class SubjectFactory(factory.django.DjangoModelFactory):
    """Factory para o modelo Subject."""

    class Meta:
        model = Subject

    name = factory.Faker("sentence", nb_words=4, locale="pt_BR")
    matrix = factory.SubFactory(MatrixFactory)
    subject_type = factory.Faker(
        "random_element",
        elements=[choice[0] for choice in Subject.SubjectsDuration.choices],
    )
    objective = factory.Faker("text", max_nb_chars=300, locale="pt_BR")
    content = factory.Faker("text", max_nb_chars=500, locale="pt_BR")
    methodology = factory.Faker("text", max_nb_chars=400, locale="pt_BR")
    resources = factory.Faker("text", max_nb_chars=300, locale="pt_BR")
    assessments = factory.Faker("text", max_nb_chars=400, locale="pt_BR")
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.SubFactory(UserFactory)

    @factory.post_generation
    def courses(self, create, extracted, **kwargs):
        """Adiciona cursos à disciplina."""
        if not create:
            return

        if extracted:
            for course in extracted:
                self.courses.add(course)
        else:
            # Cria e adiciona de 1 a 3 cursos aleatórios
            import random

            num_courses = random.randint(1, 3)  # noqa: S311
            courses = CourseFactory.create_batch(num_courses)
            for course in courses:
                self.courses.add(course)


class OfferFactory(factory.django.DjangoModelFactory):
    """Factory para o modelo Offer."""

    class Meta:
        model = Offer

    status = factory.Faker(
        "random_element",
        elements=[choice[0] for choice in Offer.OfferStatus.choices],
    )
    subject = factory.SubFactory(SubjectFactory)
    course = factory.SubFactory(CourseFactory)
    year = factory.Faker("random_int", min=2023, max=2025)
    semester = factory.Faker(
        "random_element",
        elements=[choice[0] for choice in Offer.Semester.choices],
    )
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.SubFactory(UserFactory)

    @factory.post_generation
    def teachers(self, create, extracted, **kwargs):
        """Adiciona professores à oferta."""
        if not create:
            return

        if extracted:
            for teacher in extracted:
                self.teachers.add(teacher)
        else:
            # Cria e adiciona de 1 a 2 professores aleatórios
            import random

            num_teachers = random.randint(1, 2)  # noqa: S311
            teachers = TeacherFactory.create_batch(num_teachers)
            for teacher in teachers:
                self.teachers.add(teacher)

    @classmethod
    def create_open(cls, **kwargs):
        """Cria uma oferta aberta."""
        return cls.create(status=Offer.OfferStatus.OPEN, **kwargs)

    @classmethod
    def create_closed(cls, **kwargs):
        """Cria uma oferta fechada."""
        return cls.create(status=Offer.OfferStatus.CLOSED, **kwargs)


class EnrollmentFactory(factory.django.DjangoModelFactory):
    """Factory para o modelo Enrollment."""

    class Meta:
        model = Enrollment
        django_get_or_create = ["offer", "student"]

    offer = factory.SubFactory(OfferFactory)
    student = factory.SubFactory(StudentFactory)
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.SubFactory(UserFactory)
    last_synced_at = factory.Faker(
        "date_time_this_year",
        tzinfo=timezone.get_current_timezone(),
    )

    # Notas dos bimestres (podem ser nulas)
    grade1 = factory.Faker(
        "pydecimal",
        left_digits=3,
        right_digits=0,
        min_value=0,
        max_value=100,
    )
    absences1 = factory.Faker("random_int", min=0, max=20)

    grade2 = factory.Faker(
        "pydecimal",
        left_digits=3,
        right_digits=0,
        min_value=0,
        max_value=100,
    )
    absences2 = factory.Faker("random_int", min=0, max=20)

    grade3 = factory.Faker(
        "pydecimal",
        left_digits=3,
        right_digits=0,
        min_value=0,
        max_value=100,
    )
    absences3 = factory.Faker("random_int", min=0, max=20)

    grade4 = factory.Faker(
        "pydecimal",
        left_digits=3,
        right_digits=0,
        min_value=0,
        max_value=100,
    )
    absences4 = factory.Faker("random_int", min=0, max=20)

    YearSemesterReference = factory.Faker("random_int", min=1, max=8)

    @classmethod
    def create_with_grades(cls, **kwargs):
        """Cria uma matrícula com todas as notas preenchidas."""
        return cls.create(**kwargs)

    @classmethod
    def create_without_grades(cls, **kwargs):
        """Cria uma matrícula sem notas (apenas matriculado)."""
        return cls.create(grade1=None, grade2=None, grade3=None, grade4=None, **kwargs)

    @classmethod
    def create_partial_grades(cls, bimesters=2, **kwargs):
        """Cria uma matrícula com notas apenas nos primeiros N bimestres."""
        grades = {}
        for i in range(1, 5):
            if i <= bimesters:
                continue  # Mantém a nota gerada automaticamente
            grades[f"grade{i}"] = None

        return cls.create(**grades, **kwargs)
