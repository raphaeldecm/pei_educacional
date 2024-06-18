from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Q

from sistema_pei.academics.models import Courses, Subject
from sistema_pei.educational_plan.models import Pei
from sistema_pei.people.models import Teacher

# Create your views here.


class HomePageView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filter Selectors
        context['selector_courses'] = Courses.objects.all()
        context['selector_teachers'] = Teacher.objects.all()
        context['selector_Subjects'] = Subject.objects.all()

        # Cards
        context['pending_peis'] = Pei.objects.filter(
            status='NOT_START').count()
        context['in_progress_peis'] = Pei.objects.filter(
            status='IN_PROGRESS').count()
        context['filled_peis'] = Pei.objects.filter(status='FEEDBACK').count()
        context['finished_peis'] = Pei.objects.filter(
            status='COMPLETED').count()

        # Table
        filters = {}
        if 'course' in self.request.GET:
            filters['subject__course__id'] = self.request.GET['course']
        if 'teacher' in self.request.GET:
            filters['subject__teacher__id'] = self.request.GET['teacher']
        if 'period' in self.request.GET:
            filters['subject__course__period'] = self.request.GET['period']
        if 'status' in self.request.GET:
            filters['status'] = self.request.GET['status']
        if 'subject' in self.request.GET:
            filters['subject__id'] = self.request.GET['subject']

        context['all_peis'] = Pei.objects.filter(**filters)

        if 'search' in self.request.GET:
            context['all_peis'] = context['all_peis'].filter(Q(student__name__icontains=self.request.GET['search']) | Q(student__registration__icontains=self.request.GET['search']))

        return context
