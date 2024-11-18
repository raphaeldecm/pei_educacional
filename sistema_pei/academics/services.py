import pandas as pd
from django.contrib import messages
from django.shortcuts import redirect

from sistema_pei.academics.models import Course

def import_courses_csv(self, uploaded_file):
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
                # Verifica e mapeia o turno (period)
                period = period_mapping.get(row["period"].capitalize())
                if not period:
                    raise ValueError(f"Valor inválido para 'period': {row['period']}")

                # Verifica e mapeia o tipo de duração (duration_type)
                duration_type = duration_mapping.get(row["duration_type"].capitalize())
                if not duration_type:
                    raise ValueError(f"Valor inválido para 'duration_type': {row['duration_type']}")

                # Atualiza ou cria o curso
                Course.objects.update_or_create(
                    name=row["name"],
                    defaults={
                        "course_type": row["course_type"],
                        "period": period,
                        "duration_type": duration_type,
                        "number_of_periods": row["number_of_periods"],
                    },
                )

            messages.success(self.request, _("Cursos importados com sucesso!"))

        except Exception as e:
            print(f"Erro ao processar o arquivo: {str(e)}")
            return redirect(self.success_url)
