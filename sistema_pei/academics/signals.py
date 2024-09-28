from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from sistema_pei.academics.models import Enrollment
from sistema_pei.educational_plan.models import Pei


@receiver(post_save, sender=Enrollment)
def createPeiForEnrollment(sender, instance, created, **kwargs):
    if created:
        Pei.objects.create(
            enrollment=instance,
            status=Pei.StatusChoice.NOT_START
        )

# Atualiza o status do PEI de acordo com o preenchimento do professor
@receiver(pre_save, sender=Pei)
def update_pei_status_on_update(sender, instance, **kwargs):
    if instance.pk:

        # Se marcado como concluído pelo coordenador, não faz nada
        if instance.status == Pei.StatusChoice.COMPLETED:
            print("Entrou")
            return

        fields_to_check = [
            instance.objective,
            instance.adapted_objective,
            instance.content,
            instance.adapted_content,
            instance.methodology,
            instance.adapted_methodology,
            instance.resources,
            instance.adapted_resources,
            instance.assessments,
            instance.adapted_assessments
        ]

        filled_fields = [field for field in fields_to_check if field]

        if len(filled_fields) == len(fields_to_check):
            instance.status = Pei.StatusChoice.FEEDBACK
        elif len(filled_fields) > 0:
            instance.status = Pei.StatusChoice.IN_PROGRESS
        else:
            instance.status = Pei.StatusChoice.NOT_START
