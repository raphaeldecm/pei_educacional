import django_filters
from django.utils import timezone
from django.db.models import Q

from sistema_pei.academics.models import Enrollment
from sistema_pei.academics.models import Offer


class OfferFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_by_search", label="Search")

    year = django_filters.NumberFilter(
        field_name="year",
        lookup_expr="exact",
        label="Ano",
    )
    
    semester = django_filters.ChoiceFilter(
        field_name="semester",
        choices=Offer.Semester.choices,
        label="Semestre",
    )

    class Meta:
        model = Offer
        fields = ["teacher", "subject", "semester", "year"]

    def filter_by_search(self, queryset, name, value):
        return queryset.filter(
            Q(subject__name__icontains=value) | Q(teacher__name__icontains=value),
        )

class EnrollmentFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        field_name="student__name",
        lookup_expr="icontains",
        label="Search",
    )

    class Meta:
        model = Enrollment
        fields = []
