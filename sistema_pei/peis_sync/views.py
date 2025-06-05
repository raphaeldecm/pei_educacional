from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from sistema_pei.core.mixins import TitleViewMixin

class PeisSyncView(TitleViewMixin, TemplateView):
    title = _("PEIs Sync")
    template_name = "peis_sync/app_download.html"