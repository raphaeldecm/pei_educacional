from django.conf import settings
from django.core.management import call_command, get_commands
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load database"

    def handle(self, *args, **options):
        last_name = lambda name: name.split(".")[-1]  # noqa: E731
        app_names = [last_name(name) for name in settings.LOCAL_APPS]

        call_command("migrate")
        call_command("create_admin_user")
        call_command("create_user_groups")

        for app_name in app_names:
            command_name = f"load_db_{app_name}"
            try:
                get_commands()[command_name]
                self.stdout.write(f"Loading {app_name} data...")
                call_command(f"load_db_{app_name}")
            except KeyError:
                continue
