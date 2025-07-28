from django.db import models

class AppVersion(models.Model):
    version = models.CharField(max_length=20)
    releaseDate = models.DateTimeField()

    class Meta:
        ordering = ['-releaseDate']

    def __str__(self):
        return self.version