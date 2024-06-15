from django.shortcuts import render
from django.views.generic import TemplateView

from sistema_pei.educational_plan.models import Pei

# Create your views here.

class HomePageView(TemplateView):
    template_name = "pages/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        #Cards
        context['pending_peis'] = Pei.objects.filter(status='NOT_START').count()
        context['in_progress_peis'] = Pei.objects.filter(status='IN_PROGRESS').count()
        context['filled_peis'] = Pei.objects.filter(status='FEEDBACK').count()
        context['finished_peis'] = Pei.objects.filter(status='COMPLETED').count()
        
        #Table
        context['all_peis'] = Pei.objects.all()
        
        return context