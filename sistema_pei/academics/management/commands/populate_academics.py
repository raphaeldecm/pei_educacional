"""
Comando para popular o banco de dados com dados fictícios do módulo academics.
Utilização
python manage.py populate_academics --courses 15 --matrices 20 --subjects 50 --offers 30 --enrollments 100

# Cria um conjunto balanceado e interligado
python manage.py populate_academics --full

# Limpa dados existentes e cria novos
python manage.py populate_academics --clear --full

"""  # noqa: E501

from django.core.management.base import BaseCommand
from django.db import transaction

from sistema_pei.academics.tests.factories import CourseFactory
from sistema_pei.academics.tests.factories import EnrollmentFactory
from sistema_pei.academics.tests.factories import MatrixFactory
from sistema_pei.academics.tests.factories import OfferFactory
from sistema_pei.academics.tests.factories import SubjectFactory


class Command(BaseCommand):
    """Comando para popular o banco de dados com dados fictícios do módulo academics."""

    help = (
        "Popula o banco de dados com dados fictícios (courses, matrices, subjects, "
        "offers, enrollments)"
    )

    def add_arguments(self, parser):
        """Adiciona argumentos de linha de comando."""
        parser.add_argument(
            "--courses",
            type=int,
            default=15,
            help="Número de cursos a serem criados (padrão: 15)",
        )
        parser.add_argument(
            "--matrices",
            type=int,
            default=20,
            help="Número de matrizes curriculares a serem criadas (padrão: 20)",
        )
        parser.add_argument(
            "--subjects",
            type=int,
            default=50,
            help="Número de disciplinas a serem criadas (padrão: 50)",
        )
        parser.add_argument(
            "--offers",
            type=int,
            default=30,
            help="Número de ofertas de disciplinas a serem criadas (padrão: 30)",
        )
        parser.add_argument(
            "--enrollments",
            type=int,
            default=100,
            help="Número de matrículas a serem criadas (padrão: 100)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Limpa os dados existentes antes de criar novos",
        )
        parser.add_argument(
            "--full",
            action="store_true",
            help="Cria um conjunto completo de dados interligados",
        )

    def handle(self, *args, **options):
        """Executa o comando."""
        courses_count = options["courses"]
        matrices_count = options["matrices"]
        subjects_count = options["subjects"]
        offers_count = options["offers"]
        enrollments_count = options["enrollments"]
        clear_data = options["clear"]
        full_setup = options["full"]

        if full_setup:
            # Conjunto completo de dados interligados
            courses_count = 10
            matrices_count = 15
            subjects_count = 40
            offers_count = 25
            enrollments_count = 80

        self.stdout.write(
            self.style.SUCCESS(
                f"Iniciando população do banco de dados - módulo academics:\n"
                f"- Cursos: {courses_count}\n"
                f"- Matrizes: {matrices_count}\n"
                f"- Disciplinas: {subjects_count}\n"
                f"- Ofertas: {offers_count}\n"
                f"- Matrículas: {enrollments_count}\n",
            ),
        )

        try:
            with transaction.atomic():
                # Limpa dados se solicitado
                if clear_data:
                    self._clear_data()

                # Garante que temos dados de pessoas (necessário para professores e
                # estudantes)
                self._ensure_people_data()

                # Cria os objetos usando as factories
                courses = self._create_courses(courses_count)
                matrices = self._create_matrices(matrices_count)
                subjects = self._create_subjects(subjects_count, matrices)
                offers = self._create_offers(offers_count, subjects, courses)
                self._create_enrollments(enrollments_count, offers)

            self.stdout.write(
                self.style.SUCCESS(
                    f"\n✅ População concluída com sucesso!\n"
                    f"- {len(courses)} cursos criados\n"
                    f"- {len(matrices)} matrizes criadas\n"
                    f"- {subjects_count} disciplinas criadas\n"
                    f"- {offers_count} ofertas criadas\n"
                    f"- {enrollments_count} matrículas criadas\n",
                ),
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Erro ao popular banco de dados: {e}"),
            )
            raise

    def _clear_data(self):
        """Limpa os dados existentes do módulo academics."""
        from sistema_pei.academics.models import Course
        from sistema_pei.academics.models import Enrollment
        from sistema_pei.academics.models import Matrix
        from sistema_pei.academics.models import Offer
        from sistema_pei.academics.models import Subject

        self.stdout.write("🧹 Limpando dados do módulo academics...")

        # Ordem de deleção respeitando as dependências
        Enrollment.objects.all().delete()
        Offer.objects.all().delete()
        Subject.objects.all().delete()
        Matrix.objects.all().delete()
        Course.objects.all().delete()

        self.stdout.write("✅ Dados do módulo academics limpos com sucesso!")

    def _ensure_people_data(self):
        """Garante que existem dados de pessoas necessários."""
        from sistema_pei.people.models import Student
        from sistema_pei.people.models import Teacher
        from sistema_pei.people.tests.factories import StudentFactory
        from sistema_pei.people.tests.factories import TeacherFactory

        # Verifica se existem professores
        if not Teacher.objects.exists():
            self.stdout.write("👨‍🏫 Criando professores necessários...")
            TeacherFactory.create_batch(10)

        # Verifica se existem estudantes
        if not Student.objects.exists():
            self.stdout.write("🎓 Criando estudantes necessários...")
            StudentFactory.create_batch(20)

    def _create_courses(self, count):
        """Cria cursos usando a factory."""
        if count <= 0:
            return []

        self.stdout.write(f"📚 Criando {count} cursos...")

        courses = CourseFactory.create_batch(count)

        self.stdout.write(f"✅ {len(courses)} cursos criados!")
        return courses

    def _create_matrices(self, count):
        """Cria matrizes curriculares usando a factory."""
        if count <= 0:
            return []

        self.stdout.write(f"📋 Criando {count} matrizes curriculares...")

        matrices = MatrixFactory.create_batch(count)

        self.stdout.write(f"✅ {len(matrices)} matrizes criadas!")
        return matrices

    def _create_subjects(self, count, matrices):
        """Cria disciplinas usando a factory."""
        if count <= 0:
            return

        self.stdout.write(f"📖 Criando {count} disciplinas...")

        # Cria disciplinas usando matrizes existentes se disponíveis
        if matrices:
            import random

            subjects = []
            for _ in range(count):
                matrix = random.choice(matrices)  # noqa: S311
                subject = SubjectFactory.create(matrix=matrix)
                subjects.append(subject)
        else:
            SubjectFactory.create_batch(count)

        self.stdout.write(f"✅ {count} disciplinas criadas!")

    def _create_offers(self, count, subjects_created, courses):
        """Cria ofertas de disciplinas usando a factory."""
        if count <= 0:
            return None

        self.stdout.write(f"🎯 Criando {count} ofertas de disciplinas...")

        # Cria ofertas usando cursos e disciplinas existentes se disponíveis
        from sistema_pei.academics.models import Subject

        existing_subjects = list(Subject.objects.all())

        if existing_subjects and courses:
            import random

            offers = []
            for _ in range(count):
                subject = random.choice(existing_subjects)  # noqa: S311
                course = random.choice(courses)  # noqa: S311
                offer = OfferFactory.create(subject=subject, course=course)
                offers.append(offer)
        else:
            offers = OfferFactory.create_batch(count)

        self.stdout.write(f"✅ {len(offers)} ofertas criadas!")
        return offers

    def _create_enrollments(self, count, offers):
        """Cria matrículas usando a factory."""
        if count <= 0:
            return

        self.stdout.write(f"📝 Criando {count} matrículas...")

        from sistema_pei.academics.models import Offer
        from sistema_pei.people.models import Student

        existing_offers = list(Offer.objects.all())
        existing_students = list(Student.objects.all())

        if existing_offers and existing_students:
            import random

            enrollments = []

            # Cria diferentes tipos de matrículas
            for i in range(count):
                offer = random.choice(existing_offers)  # noqa: S311
                student = random.choice(existing_students)  # noqa: S311

                # Varia os tipos de matrícula
                if i % 4 == 0:
                    # 25% sem notas
                    enrollment = EnrollmentFactory.create_without_grades(
                        offer=offer,
                        student=student,
                    )
                elif i % 4 == 1:
                    # 25% com notas parciais (2 bimestres)
                    enrollment = EnrollmentFactory.create_partial_grades(
                        bimesters=2,
                        offer=offer,
                        student=student,
                    )
                elif i % 4 == 2:
                    # 25% com notas parciais (3 bimestres)
                    enrollment = EnrollmentFactory.create_partial_grades(
                        bimesters=3,
                        offer=offer,
                        student=student,
                    )
                else:
                    # 25% com todas as notas
                    enrollment = EnrollmentFactory.create_with_grades(
                        offer=offer,
                        student=student,
                    )

                enrollments.append(enrollment)
        else:
            enrollments = EnrollmentFactory.create_batch(count)

        self.stdout.write(f"✅ {len(enrollments)} matrículas criadas!")

        # Estatísticas das matrículas criadas
        self._show_enrollment_stats()

    def _show_enrollment_stats(self):
        """Mostra estatísticas das matrículas criadas."""
        from sistema_pei.academics.models import Enrollment

        total = Enrollment.objects.count()
        with_all_grades = Enrollment.objects.filter(
            grade1__isnull=False,
            grade2__isnull=False,
            grade3__isnull=False,
            grade4__isnull=False,
        ).count()

        without_grades = Enrollment.objects.filter(
            grade1__isnull=True,
            grade2__isnull=True,
            grade3__isnull=True,
            grade4__isnull=True,
        ).count()

        self.stdout.write(
            f"📊 Estatísticas de matrículas:\n"
            f"   - Total: {total}\n"
            f"   - Com todas as notas: {with_all_grades}\n"
            f"   - Sem notas: {without_grades}\n"
            f"   - Com notas parciais: {total - with_all_grades - without_grades}",
        )
