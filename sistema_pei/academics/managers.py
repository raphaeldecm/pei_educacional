from django.db import models
from django.utils import timezone


class OfferManager(models.Manager):
    SEMESTER_SPLIT_MONTH = 6

    def current_offers(self):
        return self.filter(
            year=timezone.now().year,
            semester=1 if timezone.now().month <= self.SEMESTER_SPLIT_MONTH else 2,
        )
