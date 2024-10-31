import logging

from celery.exceptions import CeleryError
from django.db.models.signals import post_save
from django.dispatch import receiver

from sistema_pei.people.tasks import notify_teacher

from .models import Pei

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Pei)
def pei_created(sender, instance, created, **kwargs):
    if created:
        try:
            notify_teacher.delay(
                instance.enrollment.offer.teacher.id,
                subject="[Sistema PEI] Novo PEI criado.",

                message=(
                    f"Um novo PEI foi criado para a disciplina "
                    f"{instance.enrollment.offer.subject.name}."
                ),
            )
        except CeleryError as e:
            logger.exception(
                "Failed to send task to notify professor for PEI association",
                exc_info=e,
            )

