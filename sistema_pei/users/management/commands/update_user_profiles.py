from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from ...decorators import profile_groups


class Command(BaseCommand):
    help = """
        Create django groups to represent user profiles, based in models using decorator 'profile'
    """

    def handle(self, *args, **options):
        for group_name in profile_groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f"# {group} created")
        self.stdout.write("Profile groups were updated successfully")
