import os

from django.core.validators import FileExtensionValidator
from django.db import models


def apk_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    version_clean = instance.version.replace(" ", "_").replace("/", "_")
    filename = f"peis_sync_{version_clean}.{ext}"
    return os.path.join("peis-sync-apks", filename)


class AppVersion(models.Model):
    version = models.CharField(max_length=20, verbose_name="Versão")
    releaseDate = models.DateTimeField(verbose_name="Data de lançamento")
    apkFile = models.FileField(
        upload_to=apk_upload_path,
        blank=True,
        verbose_name="Arquivo de instalação APK",
        validators=[FileExtensionValidator(allowed_extensions=["apk"])],
    )

    class Meta:
        ordering = ["-releaseDate"]
        verbose_name = "Versão do App"
        verbose_name_plural = "Versões do App"

    def __str__(self):
        return self.version
