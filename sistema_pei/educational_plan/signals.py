import logging

from celery.exceptions import CeleryError
from django.db.models.signals import post_save
from django.dispatch import receiver

from sistema_pei.people.tasks import notify_teacher

from .models import Pei
from .utils import generate_pei_notification_message

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Pei)
def pei_created(sender, instance, created, **kwargs):
    if created:
        try:
            professor_name = instance.enrollment.offer.teacher.name
            subject_name = instance.enrollment.offer.subject.name
            student_name = instance.enrollment.student.name
            year_semester = instance.enrollment.YearSemesterReference

            subject, message = generate_pei_notification_message(
                professor_name, subject_name, student_name, year_semester,
            )

            notify_teacher.delay(
                instance.enrollment.offer.teacher.id,
                subject=subject,
                message=message,
            )
        except CeleryError as e:
            logger.exception(
                "Failed to send task to notify professor for PEI association",
                exc_info=e,
            )

