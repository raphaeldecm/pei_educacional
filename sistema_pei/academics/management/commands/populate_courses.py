"""
Comando para popular o banco de dados com cursos a partir de um arquivo CSV.
"""

import csv
import random

from django.conf import settings
from django.core.management.base import BaseCommand

from sistema_pei.academics.models import Course

COURSES_CSV = "{}{}".format(
    settings.APPS_DIR,
    "/academics/management/commands/course_list.csv",
)


class Command(BaseCommand):
    help = "Popula o banco de dados com cursos"

    def handle(self, *args, **kwargs):
        with open(COURSES_CSV, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                course_type = row["type"].strip()
                name = row["name"].strip() + " " + row["type"].strip()
                duracao = row["duracao"].strip()
                period = random.choice(  # noqa: S311
                    [
                        Course.CoursePeriod.MORNING,
                        Course.CoursePeriod.AFTERNOON,
                        Course.CoursePeriod.NIGHT,
                    ],
                )

                course_type_normalized = self.normalize_course_type(course_type)

                if course_type_normalized is None:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Tipo de curso desconhecido: '{course_type}', pulando entrada.",  # noqa: E501
                        ),
                    )
                    continue

                course, created = Course.objects.get_or_create(
                    name=name,
                    period=period,
                    defaults={
                        "course_type": course_type_normalized,
                        "number_of_periods": self.get_number_of_periods(duracao),
                    },
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f"Curso '{name}' criado com sucesso."),
                    )
                else:
                    self.stdout.write(self.style.WARNING(f"Curso '{name}' já existe."))

        self.stdout.write(
            self.style.SUCCESS("Cursos criados com sucesso!"),
        )

    def normalize_course_type(self, course_type):
        course_type_map = {
            "Técnico Integrado": "Técnico Integrado Regular",
            "Técnico Subsequente": "Técnico Subsequente",
            "Licenciatura": "Curso Superior de Licenciatura",
            "Tecnologia": "Curso Superior de Tecnologia",
            "Especialização": "Pós-Graduação",
            "Doutorado": "Pós-Graduação",
            "Técnico Integrado EJA": "Técnico Integrado EJA",
            "FIC": "Outros",
        }
        return course_type_map.get(course_type.strip(), None)

    def get_number_of_periods(self, duracao):
        if "quatro anos" in duracao.lower():
            return 8
        if "dois anos" in duracao.lower():
            return 4
        return 1
