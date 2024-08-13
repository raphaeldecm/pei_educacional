from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    ADMIN_NAME = "admin"
    ADMIN_EMAIL = "raphael.muniz@ifrn.edu.br"
    ADMIN_PASSWORD = (
        "argon2$argon2id$v=19$m=102400,t=2,p=8$MHFqc3lkdkIzTEhqMWs"
        "3QlNlZ0JmVA$0x4Kwnmi6EeXjaKLl9Tn+HPXF5wphUU4/i1ZxdxooDg"
    )
    help = "Adding superuser..."

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write("The superuser already exists")
        else:
            User.objects.create(
                name=self.ADMIN_NAME,
                email=self.ADMIN_EMAIL,
                password=self.ADMIN_PASSWORD,
                is_superuser=True,
                is_staff=True,
            )
