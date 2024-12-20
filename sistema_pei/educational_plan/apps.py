from django.apps import AppConfig


class EducationalPlanConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sistema_pei.educational_plan"

    def ready(self):
        pass
