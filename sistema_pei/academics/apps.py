from django.apps import AppConfig


class AcademicsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sistema_pei.academics"

    def ready(self):
        import sistema_pei.academics.signals
