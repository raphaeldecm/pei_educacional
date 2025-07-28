from django.db import models

class AppVersion(models.Model):
    version = models.CharField(max_length=20, verbose_name="Versão")
    releaseDate = models.DateTimeField(verbose_name="Data de lançamento")
    apkFile = models.FileField(upload_to="peis-sync-apks/", blank=True, verbose_name="Arquivo de instalação APK")

    class Meta:
        ordering = ['-releaseDate']
        verbose_name = "Versão do App"
        verbose_name_plural = "Versões do App"

    def __str__(self):
        return self.version