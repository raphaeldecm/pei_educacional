import django_filters
from django.db.models import Q

from sistema_pei.academics.models import Course

from .models import Campus
from .models import Student
from .models import Teacher


class TeacherFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label="Nome")
    email = django_filters.CharFilter(lookup_expr="icontains", label="E-mail")
    campus = django_filters.ModelChoiceFilter(
        queryset=Campus.objects.all(),
        label="Campus",
    )
    code = django_filters.CharFilter(lookup_expr="icontains", label="Matrícula")

    class Meta:
        model = Teacher
        fields = ["name", "email", "campus", "code"]


class StudentFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="multi_field_search", label="Search")
    course = django_filters.ModelChoiceFilter(
        queryset=Course.objects.order_by("name", "period"),
        label="Curso",
    )

    class Meta:
        model = Student
        fields = ["course"]

    def multi_field_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(registration__icontains=value),
        )
