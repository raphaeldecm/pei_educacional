import csv

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from sistema_pei.people.constants import EDUCATIONAL_NECESSITIES_CHOICES
from sistema_pei.people.models import Campus
from sistema_pei.people.models import SpecificNecessitie
from sistema_pei.people.models import Teacher

User = get_user_model()

TEACHERS_CSV = str(settings.APPS_DIR / "people" / "bin" / "DOCENTES_PF_09072024.csv")


class Command(BaseCommand):
    help = """
        Create django groups to represent.
    """

    def handle(self, *args, **options):
        for necessitie in EDUCATIONAL_NECESSITIES_CHOICES:
            SpecificNecessitie.objects.get_or_create(name=necessitie)

        for campus in self.get_campus():
            Campus.objects.get_or_create(name=campus[0], abbreviation=campus[1])

        with open(TEACHERS_CSV, encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                Teacher.objects.get_or_create(
                    name=row[0].strip(),
                    email=row[3].strip(),
                    campus=Campus.objects.get(abbreviation=row[2].strip()),
                    code=row[1].strip(),
                )

    def get_campus(self):
        return [
            ("Apodi", "AP"),
            ("Caicó", "CA"),
            ("Canguaretama", "CANG"),
            ("Ceará-Mirim", "CM"),
            ("Currais Novos", "CN"),
            ("Ipanguaçu", "IP"),
            ("João Câmara", "JC"),
            ("Jucurutu", "JUC"),
            ("Lajes", "LAJ"),
            ("Macau", "MC"),
            ("Mossoró", "MO"),
            ("Natal-Central", "CNAT"),
            ("Natal-Centro Histórico", ""),
            ("Natal-Zona Leste", "ZL"),
            ("Natal-Zona Norte", "ZN"),
            ("Nova Cruz", "NC"),
            ("Parelhas", "PAAS"),
            ("Parnamirim", "PAR"),
            ("Pau dos Ferros", "PF"),
            ("Santa Cruz", "SC"),
            ("São Gonçalo do Amarante", "SGA"),
            ("São Paulo do Potengi", "SPP"),
            ("Reitoria", "RE"),
        ]
