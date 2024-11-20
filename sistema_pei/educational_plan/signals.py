import logging

from celery.exceptions import CeleryError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from sistema_pei.educational_plan.utils import NotificationEmailContent
from sistema_pei.people.tasks import notify_teacher

from .models import Pei

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Pei)
def pei_created(sender, instance, created, **kwargs):
    if created:
        try:
            teacher = instance.responsible_teacher
            subject_name = instance.enrollment.offer.subject.name
            student_name = instance.enrollment.student.name
            year_semester = instance.enrollment.YearSemesterReference

            subject, message = NotificationEmailContent.created_pei(
                teacher.name, subject_name, student_name, year_semester,
            )

            notify_teacher.delay(
                teacher.id,
                subject=subject,
                message=message,
            )

        except CeleryError as e:
            logger.exception(
                "Failed to send task to notify professor for PEI association",
                exc_info=e,
            )

@receiver(post_delete, sender=Pei)
def pei_deleted(sender, instance, **kwargs):
    try:
        teacher = instance.responsible_teacher
        subject_name = instance.enrollment.offer.subject.name
        student_name = instance.enrollment.student.name
        year_semester = instance.enrollment.YearSemesterReference

        subject, message = NotificationEmailContent.deleted_pei(
            teacher, subject_name, student_name, year_semester,
        )

        notify_teacher.delay(
            teacher.id,
            subject=subject,
            message=message,
        )

    except CeleryError as e:
        logger.exception(
            "Failed to send task to notify professor for PEI removal",
            exc_info=e,
        )
