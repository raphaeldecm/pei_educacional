from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from sistema_pei.academics.models import Enrollment
from sistema_pei.educational_plan.models import Pei


@receiver(post_save, sender=Enrollment)
def createPeiForEnrollment(sender, instance, created, **kwargs):
    if created:
        Pei.objects.create(
            enrollment=instance,
            status=Pei.StatusChoice.NOT_START,
            objective=instance.offer.subject.objective,
            content=instance.offer.subject.content,
            methodology=instance.offer.subject.methodology,
            resources=instance.offer.subject.resources,
            assessments=instance.offer.subject.assessments
        )
