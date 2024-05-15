from collections import namedtuple

from django.conf import settings
from django.core.management import call_command, get_commands
from django.core.management.base import BaseCommand

CommandItem = namedtuple("CommandItem", ["name", "initial_message"])

COMMANDS = [
    CommandItem("migrate", "Migrating database..."),
    CommandItem("create_admin_user", "Creating superuser..."),
    CommandItem("create_user_groups", "Creating user groups..."),
    # CommandItem("load_db_..", "Loading data..."),
]

class Command(BaseCommand):
    help = "Load database"

    def handle(self, *args, **options):
        print("###", get_commands().keys())
        valid_commands = [
            command for command in COMMANDS if command.name in get_commands().keys()
        ]
        for command in valid_commands:
            self.stdout.write(command.initial_message)
            call_command(command.name)
