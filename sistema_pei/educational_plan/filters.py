import django_filters
from django.db.models import Q
from django.utils import timezone

from sistema_pei.academics import models
from sistema_pei.academics.constants import COURSE_TYPE
from sistema_pei.educational_plan.models import Pei
from sistema_pei.people.models import Teacher

class PeiFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='multi_field_search', label="Search")

    course = django_filters.ModelChoiceFilter(
        queryset=models.Course.objects.all(),
        field_name='enrollment__offer__course',
        label="course"
    )

    subject = django_filters.ModelChoiceFilter(
        queryset=models.Subject.objects.all(),
        field_name='enrollment__offer__subject',
        label="subject"
    )

    teacher = django_filters.ModelChoiceFilter(
        queryset=Teacher.objects.all(),
        field_name='enrollment__offer__teacher',
        label="teacher",
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            try:
                teacher = Teacher.objects.get(email=user.email)
                self.filters['teacher'].initial = teacher
            except Teacher.DoesNotExist:
                pass


    class Meta:
        model = Pei
        fields = ['status', 'teacher']

    def multi_field_search(self, queryset, name, value):
        return queryset.filter(
            Q(enrollment__student__name__icontains=value) |
            Q(enrollment__student__registration__icontains=value)
        )
