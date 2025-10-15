import pandas as pd
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

from sistema_pei.academics.models import Course
from sistema_pei.people.models import Campus
from sistema_pei.people.models import Student
from sistema_pei.people.models import Teacher
from sistema_pei.users.models import User


def import_student_csv(self, uploaded_file):
    insert_counter = 0
    error_counter = 0

    try:
        data = pd.read_csv(uploaded_file, encoding="utf-8")

        data.columns = data.columns.str.strip().str.lower()

        required_columns = {
            "nome",
            "e-mail",
            "curso",
            "matrícula",
            "período de referência (periodo atual do aluno)",
            "necessidades especiais específicas",
            "histórico",
            "necessidades educacionais especificas",
            "aptidão e dificuldades apresentadas",
            "dificuldades",
            "outras necessidades educacionais especificas do(a) estudante",
            "questões geradoras para criação do pei/adaptações",
        }

        if not required_columns.issubset(data.columns):
            missing_columns = required_columns - set(data.columns)
            messages.error(
                self.request,
                "O arquivo CSV está faltando as seguintes colunas: "
                + ", ".join(missing_columns),
            )
            return redirect(self.success_url)

        default_image_path = static("images/img/login-cover.webp")

        for _index, row in data.iterrows():
            try:
                course = Course.objects.filter(name=row["curso"]).first()
                if not course:
                    error_counter += 1
                    continue

                Student.objects.update_or_create(
                    email=row["e-mail"],
                    defaults={
                        "name": row["nome"],
                        "registration": row["matrícula"],
                        "personal_history": row["histórico"],
                        "specific_necessities": row[
                            "necessidades especiais específicas"
                        ],
                        "general_necessitie": row[
                            "outras necessidades educacionais especificas do(a) estudante"
                        ],
                        "creation_reasons": row[
                            "questões geradoras para criação do pei/adaptações"
                        ],
                        "dificulties": row["dificuldades"],
                        "abilities": row["aptidão e dificuldades apresentadas"],
                        "course": course,
                        "reference_period": row[
                            "período de referência (periodo atual do aluno)"
                        ],
                        "sectors": [User.Sector.NAPNE],
                        "image": default_image_path,
                    },
                )
                insert_counter += 1

            except Exception:
                error_counter += 1
                continue

        success_message = f"Discentes inseridos: {insert_counter}, Discentes com erro: {error_counter}"
        messages.success(self.request, success_message)
        return redirect(self.success_url)

    except Exception as e:
        error_message = f"Erro ao processar o arquivo:\n{e}"
        messages.error(self.request, error_message)
        return redirect(self.success_url)


def teachers_import(self, uploaded_file):
    errors = 0
    error_counter = 0
    insert_counter = 0

    try:
        data = pd.read_csv(uploaded_file, encoding="utf-8")

        required_fields = {"nome", "email", "matricula", "campus"}

        if not required_fields.issubset(data.columns):
            missing_columns = required_fields - set(data.columns)
            messages.error(
                self.request,
                _("O arquivo CSV está faltando as seguintes colunas: ")
                + ", ".join(missing_columns),
            )
            return redirect(self.success_url)

        for _index, row in data.iterrows():
            # validar o formato do email
            try:
                email = row["email"]
                validate_email(email)
            except ValidationError:
                messages.error(
                    self.request,
                    _("O campo 'email' não é um email válido."),
                )
                errors += 1
                return redirect(self.success_url)

            # validar o formato da matrícula
            try:
                matricula = row["matricula"]
                int(matricula)
            except ValueError:
                messages.error(
                    self.request,
                    _("O campo 'matricula' não é um número inteiro."),
                )
                errors += 1
                return redirect(self.success_url)

            # validar o campus
            campus_name = row["campus"]
            if campus_name.lower() not in [
                campus.name.lower() for campus in Campus.objects.all()
            ]:
                messages.error(self.request, _("O campus enviado não é valido."))
                errors += 1
                return redirect(self.success_url)
            else:
                campus = Campus.objects.get(name__icontains=campus_name)

            if errors != 0:
                error_counter += 1
            else:
                Teacher.objects.update_or_create(
                    name=row["nome"],
                    email=email,
                    code=matricula,
                    campus=campus,
                )
                insert_counter += 1

        success_message = f"Docentes inseridos: {insert_counter},' \
        'Docentes com erros: {error_counter}"
        messages.success(self.request, success_message)

        return redirect(self.success_url)

    except Exception as e:
        messages.error(self.request, f"Erro ao importar arquivo: {e!s}")
        return redirect(self.success_url)
