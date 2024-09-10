import factory

from sistema_pei.academics.models import Course


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    name = factory.Faker("word")
    course_type = factory.Iterator(
        ["Técnico Integrado Regular", "Técnico Subsequente",
         "Curso Superior de Licenciatura", "Pós-Graduação", "Técnico Integrado EJA",
         "Curso Superior de Tecnologia", "Engenharia", "Outros"],
    )
    period = factory.Iterator(["Matutino", "Vespertino", "Noturno", "Integral"])
    duration_type = factory.Iterator(["Anos", "Semestres"])
    number_of_periods = factory.Faker("random_int", min=2, max=10)

