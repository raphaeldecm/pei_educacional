from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from sistema_pei.core.mixins import TitleViewMixin
from sistema_pei.peis_sync.models import AppVersion

class PeisSyncView(TitleViewMixin, TemplateView):
    title = _("PEIs Sync")
    template_name = "peis_sync/app_download.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_apk_version = AppVersion.objects.exclude(apkFile="").exclude(apkFile__isnull=True).order_by('-releaseDate').first()
        context['latestVersion'] = latest_apk_version
        return context