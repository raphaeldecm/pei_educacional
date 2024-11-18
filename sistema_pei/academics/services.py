import pandas as pd
from django.contrib import messages
from django.shortcuts import redirect

from sistema_pei.academics.models import Course

def import_courses_csv(self, uploaded_file):
    insert_counter = 0
    error_counter = 0

    try:
        data = pd.read_csv(uploaded_file)

        required_columns = {"name", "period", "course_type", "duration_type", "number_of_periods"}

        if not required_columns.issubset(data.columns):
            missing_columns = required_columns - set(data.columns)
            messages.error(self.request, _("O arquivo CSV está faltando as seguintes colunas: ") + ", ".join(missing_columns))
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

        for _, row in data.iterrows():
            try:
                period = period_mapping.get(row["period"].capitalize())
                if not period:
                    error_counter += 1
                    continue

                duration_type = duration_mapping.get(row["duration_type"].capitalize())
                if not duration_type:
                    error_counter += 1
                    continue

                Course.objects.update_or_create(
                    name=row["name"],
                    defaults={
                        "course_type": row["course_type"],
                        "period": period,
                        "duration_type": duration_type,
                        "number_of_periods": row["number_of_periods"],
                    },
                )
                insert_counter += 1

            except Exception as e:
                error_counter += 1
                continue


        success_message = f"Cursos inseridos: {insert_counter}, Cursos com erro: {error_counter}"
        messages.success(self.request, success_message)

        return redirect(self.success_url)

    except Exception as e:
        error_message = f"Erro ao processar o arquivo:\n{str(e)}"
        messages.error(self.request, error_message)
        return redirect(self.success_url)





