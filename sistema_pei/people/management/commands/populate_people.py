"""

Comando para popular o banco de dados com dados fictícios usando as factories.

Utilização
python manage.py populate_people --teachers 20 --responsibles 25 --students 50

Reset completo
python manage.py populate_people --clear --teachers 10 --responsibles 15 --students 25

"""

from django.core.management.base import BaseCommand
from django.db import transaction

from sistema_pei.people.models import Campus
from sistema_pei.people.models import SpecificNecessitie
from sistema_pei.people.tests.factories import CampusFactory
from sistema_pei.people.tests.factories import ResponsibleFactory
from sistema_pei.people.tests.factories import SpecificNecessitieFactory
from sistema_pei.people.tests.factories import StudentFactory
from sistema_pei.people.tests.factories import TeacherFactory


class Command(BaseCommand):
    help = (
        "Popula o banco de dados com pessoas fictícias (teachers, responsibles, "
        "students)"
    )

    def add_arguments(self, parser):
        """Argumentos de linha de comando."""
        parser.add_argument(
            "--teachers",
            type=int,
            default=10,
            help="Número de professores a serem criados (padrão: 10)",
        )
        parser.add_argument(
            "--responsibles",
            type=int,
            default=15,
            help="Número de responsáveis a serem criados (padrão: 15)",
        )
        parser.add_argument(
            "--students",
            type=int,
            default=25,
            help="Número de estudantes a serem criados (padrão: 25)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Limpa os dados existentes antes de criar novos",
        )

    def handle(self, *args, **options):
        """Executa o comando."""
        teachers_count = options["teachers"]
        responsibles_count = options["responsibles"]
        students_count = options["students"]
        clear_data = options["clear"]

        self.stdout.write(
            self.style.SUCCESS(
                f"Iniciando população do banco de dados:\n"
                f"- Professores: {teachers_count}\n"
                f"- Responsáveis: {responsibles_count}\n"
                f"- Estudantes: {students_count}\n",
            ),
        )

        try:
            with transaction.atomic():
                # Limpa dados se solicitado
                if clear_data:
                    self._clear_data()

                # Garante que temos campi e necessidades específicas
                self._ensure_base_data()

                # Cria os objetos usando as factories
                self._create_teachers(teachers_count)
                self._create_responsibles(responsibles_count)
                self._create_students(students_count)

            self.stdout.write(
                self.style.SUCCESS(
                    f"\n✅ População concluída com sucesso!\n"
                    f"- {teachers_count} professores criados\n"
                    f"- {responsibles_count} responsáveis criados\n"
                    f"- {students_count} estudantes criados\n",
                ),
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Erro ao popular banco de dados: {e}"),
            )
            raise

    def _clear_data(self):
        """Limpa os dados existentes."""
        from sistema_pei.people.models import Responsible
        from sistema_pei.people.models import Student
        from sistema_pei.people.models import Teacher

        self.stdout.write("🧹 Limpando dados existentes...")

        Student.objects.all().delete()
        Teacher.objects.all().delete()
        Responsible.objects.all().delete()

        self.stdout.write("✅ Dados limpos com sucesso!")

    def _ensure_base_data(self):
        """Garante que existem dados base necessários (campi e necessidades)."""
        self.stdout.write("📋 Verificando dados base...")

        # Cria alguns campi se não existirem
        if not Campus.objects.exists():
            self.stdout.write("- Criando campi...")
            CampusFactory.create_batch(5)

        # Cria algumas necessidades específicas se não existirem
        if not SpecificNecessitie.objects.exists():
            self.stdout.write("- Criando necessidades específicas...")
            SpecificNecessitieFactory.create_batch(10)

    def _create_teachers(self, count):
        """Cria professores usando a factory."""
        if count <= 0:
            return

        self.stdout.write(f"👨‍🏫 Criando {count} professores...")

        teachers = TeacherFactory.create_batch(count)

        self.stdout.write(f"✅ {len(teachers)} professores criados!")

    def _create_responsibles(self, count):
        """Cria responsáveis usando a factory."""
        if count <= 0:
            return

        self.stdout.write(f"👥 Criando {count} responsáveis...")

        responsibles = ResponsibleFactory.create_batch(count)

        self.stdout.write(f"✅ {len(responsibles)} responsáveis criados!")

    def _create_students(self, count):
        """Cria estudantes usando a factory."""
        if count <= 0:
            return

        self.stdout.write(f"🎓 Criando {count} estudantes...")

        students = StudentFactory.create_batch(count)

        self.stdout.write(f"✅ {len(students)} estudantes criados!")
