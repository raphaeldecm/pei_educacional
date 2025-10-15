from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import m2m_changed
from django.db.models.signals import pre_save
from django.dispatch import receiver

from sistema_pei.educational_plan.utils import NotificationEmailContent
from sistema_pei.people.models import Notification
from sistema_pei.people.models import Student
from sistema_pei.people.models import Teacher
from sistema_pei.people.tasks import notify_teacher_email


@receiver(pre_save, sender=Student)
def fields_changed(sender, instance, **kwargs):
    # Verifica se o objeto já existe no banco de dados
    if instance.pk:
        try:
            previous_instance = Student.objects.get(pk=instance.pk)
        except ObjectDoesNotExist:
            return

        # Verifica alterações em campos específicos
        altered_fields = {}
        if previous_instance.personal_history != instance.personal_history:
            altered_fields["personal_history"] = (
                previous_instance.personal_history,
                instance.personal_history,
            )
        if previous_instance.general_necessitie != instance.general_necessitie:
            altered_fields["general_necessitie"] = (
                previous_instance.general_necessitie,
                instance.general_necessitie,
            )
        if previous_instance.creation_reasons != instance.creation_reasons:
            altered_fields["creation_reasons"] = (
                previous_instance.creation_reasons,
                instance.creation_reasons,
            )
        if previous_instance.abilities != instance.abilities:
            altered_fields["abilities"] = (
                previous_instance.abilities,
                instance.abilities,
            )
        if previous_instance.dificulties != instance.dificulties:
            altered_fields["dificulties"] = (
                previous_instance.dificulties,
                instance.dificulties,
            )
        if previous_instance.specific_necessities != instance.specific_necessities:
            altered_fields["specific_necessities"] = (
                previous_instance.specific_necessities,
                instance.specific_necessities,
            )

        # Exibe ou processa as alterações, se houver alguma
        if altered_fields:
            teachersList = Teacher.objects.filter(
                offers__enrollments__student_id=instance.id,
            ).distinct()

            for teacher in teachersList:
                subject, message = NotificationEmailContent.changed_history(
                    teacher.name,
                    instance.name,
                )

                notify_teacher_email.delay(
                    teacher.id,
                    subject=subject,
                    message=message,
                )

                Notification.objects.create(
                    title="Historico de um aluno foi alterado!",
                    text=(
                        f"O histórico do aluno {instance.name} foi alterado. "
                        "Verfique o perfil do aluno para mais detalhes."
                    ),
                    user=teacher.user,
                    type="Alert",
                    action=f"/people/profile/{instance.id}?tab=historic#tab",
                )


@receiver(m2m_changed, sender=Student.educational_necessities.through)
def educational_necessities_changed(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        teachersList = Teacher.objects.filter(
            offers__enrollments__student_id=instance.id,
        ).distinct()

        for teacher in teachersList:
            subject, message = NotificationEmailContent.changed_history(
                teacher.name,
                instance.name,
            )

            notify_teacher_email.delay(
                teacher.id,
                subject=subject,
                message=message,
            )

            Notification.objects.create(
                title="Necessidades Específicas de um aluno foram alteradas!",
                text=f"As necessidades educacionais específicas do aluno {instance.name} foram alteradas. Verfique o perfil do aluno para mais detalhes.",  # noqa: E501
                user=teacher.user,
                type="Alert",
                action=f"/people/profile/{instance.id}",
            )
