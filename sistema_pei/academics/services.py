import pandas as pd
from django.contrib import messages
from django.shortcuts import redirect

from sistema_pei.academics.models import Course
from sistema_pei.academics.models import Subject


def import_courses_csv(self, uploaded_file):
    insert_counter = 0
    error_counter = 0

    try:
        data = pd.read_csv(uploaded_file)

        required_columns = {
            "Nome",
            "Tipo do Curso",
            "Turno",
            "Tipo de duração",
            "Quantidade de periodos",
        }
        if not required_columns.issubset(data.columns):
            missing_columns = required_columns - set(data.columns)
            messages.error(
                self.request,
                "O arquivo CSV está faltando as seguintes colunas: "
                + ", ".join(missing_columns),
            )
            return redirect(self.success_url)

        period_mapping = {
            "Matutino": Course.CoursePeriod.MORNING,
            "Vespertino": Course.CoursePeriod.AFTERNOON,
            "Noturno": Course.CoursePeriod.NIGHT,
        }
        duration_mapping = {
            "Semestral": Course.CourseDurationType.SEMESTER,
            "Anual": Course.CourseDurationType.YEAR,
        }

        for index, row in data.iterrows():  # noqa: B007
            try:
                period = period_mapping.get(row["Turno"])
                if not period:
                    error_counter += 1
                    continue

                duration_type = duration_mapping.get(row["Tipo de duração"])
                if not duration_type:
                    error_counter += 1
                    continue

                Course.objects.update_or_create(
                    name=row["Nome"],
                    defaults={
                        "course_type": row["Tipo do Curso"],
                        "period": period,
                        "duration_type": duration_type,
                        "number_of_periods": row["Quantidade de periodos"],
                    },
                )
                insert_counter += 1

            except Exception:
                error_counter += 1
                continue

        success_message = (
            f"Cursos inseridos: {insert_counter}, Cursos com erro: {error_counter}"
        )
        messages.success(self.request, success_message)
        return redirect(self.success_url)

    except Exception as e:
        error_message = f"Erro ao processar o arquivo:\n{e}"
        messages.error(self.request, error_message)
        return redirect(self.success_url)


def import_subject_csv(self, uploaded_file):
    insert_counter = 0
    error_counter = 0

    try:
        data = pd.read_csv(uploaded_file)

        required_columns = {
            "Nome",
            "Duração",
            "Objetivos da disciplina",
            "Conteúdo programático",
            "Metodologias",
            "Recursos didáticos",
            "Avaliações",
        }

        if not required_columns.issubset(data.columns):
            missing_columns = required_columns - set(data.columns)
            messages.error(
                self.request,
                "O arquivo CSV está faltando as seguintes colunas: "
                + ", ".join(missing_columns),
            )
            return redirect(self.success_url)

        duration_mapping = {
            "Semestral": Subject.SubjectsDuration.SEMESTER,
            "Anual": Subject.SubjectsDuration.YEAR,
        }

        for index, row in data.iterrows():  # noqa: B007
            try:
                subject_type = duration_mapping.get(row["Duração"])
                if not subject_type:
                    error_counter += 1
                    continue

                Subject.objects.update_or_create(
                    name=row["Nome"],
                    defaults={
                        "subject_type": subject_type,
                        "objective": row["Objetivos da disciplina"],
                        "content": row["Conteúdo programático"],
                        "methodology": row["Metodologias"],
                        "resources": row["Recursos didáticos"],
                        "assessments": row["Avaliações"],
                    },
                )
                insert_counter += 1

            except Exception:
                error_counter += 1
                continue

        success_message = (
            f"Disciplinas inseridas: {insert_counter}, "
            f"Disciplinas com erro: {error_counter}"
        )
        messages.success(self.request, success_message)

        return redirect(self.success_url)

    except Exception as e:
        error_message = f"Erro ao processar o arquivo:\n{e}"
        messages.error(self.request, error_message)
        return redirect(self.success_url)
