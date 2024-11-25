import pandas as pd
from django.contrib import messages
from django.shortcuts import redirect

from sistema_pei.academics.models import Course, Subject
from sistema_pei.people.models import Student
from sistema_pei.users.models import User

from django.templatetags.static import static

def import_student_csv(self, uploaded_file):
    insert_counter = 0
    error_counter = 0

    try:
        data = pd.read_csv(uploaded_file)

        required_columns = {
            "Nome",
            "E-mail",
            "Curso",
            "Matrícula",
            "Período de Referência (Periodo atual do aluno)",
            "Necessidades especiais específicas",
            "Histórico",
            "Necessidades Educacionais Especificas",
            "Aptidão e dificuldades Apresentadas",
            "Dificuldades",
            "Outras necessidades educacionais especificas do(a) estudante",
            "Questões Geradoras para criação do pei/Adaptações",
        }

        if not required_columns.issubset(data.columns):
            missing_columns = required_columns - set(data.columns)
            messages.error(
                self.request,
                "O arquivo CSV está faltando as seguintes colunas: " + ", ".join(missing_columns)
            )
            return redirect(self.success_url)

        default_image_path = static("images/img/login-cover.webp")

        for index, row in data.iterrows():
            try:
                course = Course.objects.filter(name=row["Curso"]).first()
                if not course:
                    error_counter += 1
                    continue

                Student.objects.update_or_create(
                    email=row["E-mail"],
                    defaults={
                        "name": row["Nome"],
                        "registration": row["Matrícula"],
                        "personal_history": row["Histórico"],
                        "specific_necessities": row["Necessidades especiais específicas"],
                        "general_necessitie": row["Outras necessidades educacionais especificas do(a) estudante"],
                        "creation_reasons": row["Questões Geradoras para criação do pei/Adaptações"],
                        "dificulties": row["Dificuldades"],
                        "abilities": row["Aptidão e dificuldades Apresentadas"],
                        "course": course,
                        "reference_period": row["Período de Referência (Periodo atual do aluno)"],
                        "sectors": [User.Sector.NAPNE],
                        "image": default_image_path,
                    },
                )
                insert_counter += 1

            except Exception:
                error_counter += 1
                continue

        success_message = f"Estudantes inseridos: {insert_counter}, Estudantes com erro: {error_counter}"
        messages.success(self.request, success_message)
        return redirect(self.success_url)

    except Exception as e:
        error_message = f"Erro ao processar o arquivo:\n{e}"
        messages.error(self.request, error_message)
        return redirect(self.success_url)

