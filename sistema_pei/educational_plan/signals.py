import logging

from celery.exceptions import CeleryError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from sistema_pei.educational_plan.utils import NotificationEmailContent
from sistema_pei.people.models import Notification
from sistema_pei.people.tasks import notify_teacher_email

from .models import Pei

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Pei)
def pei_created(sender, instance, created, **kwargs):
    if created:
        try:
            professor_name = instance.enrollment.offer.teacher.name
            subject_name = instance.enrollment.offer.subject.name
            student_name = instance.enrollment.student.name
            year_semester = instance.enrollment.YearSemesterReference

            subject, message = NotificationEmailContent.created_pei(
                professor_name, subject_name, student_name, year_semester,
            )

            notify_teacher_email.delay(
                instance.enrollment.offer.teacher.id,
                subject=subject,
                message=message,
            )
            
            Notification.objects.create(
                title="Novo PEI adicionado!",
                text=f"O PEI do aluno {student_name}, na disciplina {subject_name} - {year_semester} foi adicionado, e você é o responsável.",
                user=instance.enrollment.offer.teacher.user,
                type="Alert"
            )
            
        except CeleryError as e:
            logger.exception(
                "Failed to send task to notify professor for PEI association",
                exc_info=e,
            )

@receiver(post_delete, sender=Pei)
def pei_deleted(sender, instance, **kwargs):
    try:
        professor_name = instance.enrollment.offer.teacher.name
        subject_name = instance.enrollment.offer.subject.name
        student_name = instance.enrollment.student.name
        year_semester = instance.enrollment.YearSemesterReference

        subject, message = NotificationEmailContent.deleted_pei(
            professor_name, subject_name, student_name, year_semester,
        )

        notify_teacher_email.delay(
            instance.enrollment.offer.teacher.id,
            subject=subject,
            message=message,
        )
        
        Notification.objects.create(
            title="PEI removido!",
            text=f"O PEI do aluno {student_name}, na disciplina {subject_name} - {year_semester}, que você estava participando foi removido pelo coordenador.",
            user=instance.enrollment.offer.teacher.user,
            type="Alert"
        )

    except CeleryError as e:
        logger.exception(
            "Failed to send task to notify professor for PEI removal",
            exc_info=e,
        )
