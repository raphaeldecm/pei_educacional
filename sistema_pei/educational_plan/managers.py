from django.db import models
from django.utils import timezone


class PeiManager(models.Manager):
    SEMESTER_SPLIT_MONTH = 6

    def current_peis(self):
        return self.filter(
            enrollment__offer__year=timezone.now().year,
            enrollment__offer__semester=1 if timezone.now().month <= self.SEMESTER_SPLIT_MONTH else 2,
        )
