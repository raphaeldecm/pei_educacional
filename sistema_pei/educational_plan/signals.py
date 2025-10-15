import logging

from celery.exceptions import CeleryError
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver

from sistema_pei.educational_plan.models import Comment
from sistema_pei.educational_plan.utils import NotificationEmailContent
from sistema_pei.people.models import Notification
from sistema_pei.people.tasks import notify_teacher_email

from .models import Answer
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
                teacher.name,
                subject_name,
                student_name,
                year_semester,
            )

            notify_teacher_email.delay(
                teacher.id,
                subject=subject,
                message=message,
            )

            Notification.objects.create(
                title="Novo PEI adicionado!",
                text=f"O PEI do aluno {student_name}, na disciplina {subject_name} - {year_semester} foi adicionado, e você é o responsável.",
                user=teacher.user,
                type="Alert",
                action=f"/educational_plan/peis/detail/{instance.id}",
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
            teacher,
            subject_name,
            student_name,
            year_semester,
        )

        notify_teacher_email.delay(
            teacher.id,
            subject=subject,
            message=message,
        )

        Notification.objects.create(
            title="PEI removido!",
            text=f"O PEI do aluno {student_name}, na disciplina {subject_name} - {year_semester}, que você estava participando foi removido pelo coordenador.",
            user=teacher.user,
            type="Alert",
            action="/educational_plan/peis/list/",
        )

    except CeleryError as e:
        logger.exception(
            "Failed to send task to notify professor for PEI removal",
            exc_info=e,
        )


@receiver(post_save, sender=Comment)
def pei_created(sender, instance, created, **kwargs):
    if created:
        try:
            teacher = instance.pei.responsible_teacher
            author = instance.created_by

            # Não não notificar caso o próprio usuário/professor criou o comentário
            if teacher.user.id == author.id:
                return

            Notification.objects.create(
                title=f"Novo comentário em PEI do aluno {instance.pei.enrollment.student}",
                text=f"{author.name} comentou no PEI da disciplina {instance.pei.enrollment.offer.subject}: {instance.text}",
                user=teacher.user,
                type="Alert",
                action=f"/educational_plan/peis/detail/{instance.id}",
            )

        except CeleryError as e:
            logger.exception(
                "Failed to send task to notify professor for PEI association",
                exc_info=e,
            )


@receiver(post_save, sender=Answer)
def pei_created(sender, instance, created, **kwargs):
    if created:
        try:
            teacher = instance.comment.pei.responsible_teacher
            author = instance.created_by

            # Não notificar caso o professor que criou a resposta seja o mesmo que criou o comentário
            if teacher.user.id == author.id:
                return

            subject = instance.comment.pei.enrollment.offer.subject
            student = instance.comment.pei.enrollment.student

            subject, message = NotificationEmailContent.created_answer(
                teacher.name,
                subject.name,
                student.name,
            )

            notify_teacher_email.delay(
                teacher.id,
                subject=subject,
                message=message,
            )

            Notification.objects.create(
                title=f"Usuário {author.name} respondeu seu comentário",
                text=f"{instance.comment.created_by.name}: {instance.comment.text} >>> {instance.created_by.name}: {instance.text}",
                user=teacher.user,
                type="Alert",
                action=f"/educational_plan/peis/detail/{instance.id}",
            )

        except CeleryError as e:
            logger.exception(
                "Failed to send task to notify professor for PEI association",
                exc_info=e,
            )
