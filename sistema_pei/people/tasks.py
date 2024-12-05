from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models import Count
from celery.exceptions import CeleryError

from sistema_pei.educational_plan.models import Pei

from sistema_pei.people.models import Notification, Teacher
from sistema_pei.educational_plan.utils import NotificationEmailContent

from celery import shared_task

@shared_task
def notify_teacher_email(teacher_id, subject, message):
        recipient = get_object_or_404(Teacher, id=teacher_id)
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient.email],
            fail_silently=False,
        )

@shared_task
def send_monthly_pei():
    try:
        # Filtra PEIs não finalizados
        pending_peis = (
            Pei.objects.filter(
                status__in=[Pei.StatusChoice.NOT_START, Pei.StatusChoice.IN_PROGRESS]
            )
            .values('responsible_teacher')
            .annotate(total_pending=Count('id'))
        )

        # Envia uma notificação para cada professor com PEIs pendentes
        for pei_info in pending_peis:
            teacher_id = pei_info['responsible_teacher']
            total_pending = pei_info['total_pending']
            teacher = Teacher.objects.get(id=teacher_id)

            subject, message = NotificationEmailContent.monthly_pei(
                teacher.name, total_pending
            )

            notify_teacher_email.delay(
                teacher.user.id,
                subject=subject,
                message=message,
            )

            Notification.objects.create(
                title="Há PEIs com preenchimento pendente!",
                text=f"Você tem {total_pending} PEIs que ainda precisam ser preenchidos. Por favor, revise os PEIs pendentes.",
                user=teacher.user,
                type="Alert"
            )

    except CeleryError as e:
        print("Falha ao enviar notificação mensal de PEIs pendentes.", exc_info=e)
