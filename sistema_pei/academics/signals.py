from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save
from django.dispatch import receiver

from sistema_pei.academics.models import Enrollment
from sistema_pei.academics.models import Offer
from sistema_pei.educational_plan.models import Pei


@receiver(post_save, sender=Enrollment)
def createPeiForEnrollment(sender, instance, created, **kwargs):
    if created:
        for teacher in instance.offer.teachers.all():
            # Verifica se já existe um PEI para esse teacher e enrollment
            if not Pei.objects.filter(
                responsible_teacher=teacher, enrollment=instance
            ).exists():
                Pei.objects.create(
                    enrollment=instance,
                    responsible_teacher=teacher,
                    status=Pei.StatusChoice.NOT_START,
                    created_by=instance.created_by,
                    updated_by=instance.updated_by,
                )


@receiver(m2m_changed, sender=Offer.teachers.through)
def createPeiForNewTeachers(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add":
        for teacher_id in pk_set:
            teacher = model.objects.get(id=teacher_id)
            for enrollment in instance.enrollments.all():
                # Verifica se já existe um PEI para esse teacher e enrollment
                if not Pei.objects.filter(
                    responsible_teacher=teacher, enrollment=enrollment
                ).exists():
                    Pei.objects.create(
                        enrollment=enrollment,
                        responsible_teacher=teacher,
                        status=Pei.StatusChoice.NOT_START,
                        created_by=enrollment.created_by,
                        updated_by=enrollment.updated_by,
                    )
