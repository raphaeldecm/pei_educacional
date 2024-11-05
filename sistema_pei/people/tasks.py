from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from .models import Teacher


@shared_task
def notify_teacher(teacher_id, subject, message):
        recipient = get_object_or_404(Teacher, id=teacher_id)
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient.email],
            fail_silently=False,
        )
