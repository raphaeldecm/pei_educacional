from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    ADMIN_USERNAME = "admin"
    ADMIN_EMAIL = "lucas.dantas@ifrn.edu.br"
    help = "Adding superuser..."

    def handle(self, *args, **options):
        exists = User.objects.filter(is_superuser=True).exists()

        if exists:
            self.stdout.write("The superuser already exists")
        else:
            User.objects.create(
                username=self.ADMIN_USERNAME,
                email=self.ADMIN_EMAIL,
                password=(
                    "argon2$argon2id$v=19$m=102400,t=2,p=8$MEJKZWgxQWNPelJZaF"
                    "Y3VktvZUlCQw$A0+Q1su1qKG/p5k651ay1tBtDdxrVDZIr/yvU0zc/30"
                ),
                is_superuser=True,
                is_staff=True,
            )
