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
        field_name='enrollment__offer__teachers',
        label="teacher",
    )

    SEMESTER_SPLIT_MONTH = 6

    year = django_filters.NumberFilter(
        field_name='enrollment__offer__year',
        lookup_expr="exact",
        label="Ano",
        initial=timezone.now().date().year,
    )

    semester = django_filters.ChoiceFilter(
        field_name='enrollment__offer__semester',
        choices=models.Offer.Semester.choices,
        label="Semestre",
        initial=1 if timezone.now().date().month <= SEMESTER_SPLIT_MONTH else 2,
    )


    class Meta:
        model = Pei
        fields = ['status']

    def multi_field_search(self, queryset, name, value):
        return queryset.filter(
            Q(enrollment__student__name__icontains=value) |
            Q(enrollment__student__registration__icontains=value)
        )
