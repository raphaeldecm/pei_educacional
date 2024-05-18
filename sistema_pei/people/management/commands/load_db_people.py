from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from sistema_pei.people.constants import EDUCATIONAL_NECESSITIES_CHOICES
from sistema_pei.people.models import SpecificNecessitie

User = get_user_model()


class Command(BaseCommand):
    help = """
        Create django groups to represent.
    """

    def handle(self, *args, **options):
        [
            SpecificNecessitie.objects.get_or_create(name=necessitie)
            for necessitie in EDUCATIONAL_NECESSITIES_CHOICES
        ]
