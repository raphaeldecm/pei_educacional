import django_filters
from django.db.models import Q
from django.utils import timezone

from sistema_pei.academics import models
from sistema_pei.academics.constants import COURSE_TYPE


class CourseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label="Nome")
    course_type = django_filters.ChoiceFilter(
        choices=COURSE_TYPE,
        label="Tipo",
    )
    period = django_filters.ChoiceFilter(
        choices=models.Course.CoursePeriod.choices,
        label="Turno",
    )
    duration_type = django_filters.ChoiceFilter(
        choices=models.Course.CourseDurationType.choices,
        label="Tipo de duração",
    )
    number_of_periods = django_filters.NumberFilter(label="Número de períodos/Anos")

    class Meta:
        model = models.Course
        fields = ["name", "course_type", "period", "duration_type", "number_of_periods"]


class OfferFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_by_search", label="Search")
    SEMESTER_SPLIT_MONTH = 6

    year = django_filters.NumberFilter(
        field_name="year",
        lookup_expr="exact",
        label="Ano",
        initial=timezone.now().date().year,
    )

    semester = django_filters.ChoiceFilter(
        field_name="semester",
        choices=models.Offer.Semester.choices,
        label="Semestre",
        required=False,
    )

    class Meta:
        model = models.Offer
        fields = ["teachers", "subject", "semester", "year"]

    def filter_by_search(self, queryset, name, value):
        return queryset.filter(
            Q(subject__name__icontains=value) | Q(teachers__name__icontains=value),
        )

class EnrollmentFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        field_name="student__name",
        lookup_expr="icontains",
        label="Search",
    )

    class Meta:
        model = models.Enrollment
        fields = []


class SubjectFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label="Search",
    )

    courses = django_filters.ModelChoiceFilter(
        queryset=models.Course.objects.all(),
        field_name="courses",
        label="Courses",
    )

    class Meta:
        model = models.Subject
        fields = ["name", "subject_type", "courses"]
