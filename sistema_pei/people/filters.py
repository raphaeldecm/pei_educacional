import django_filters

from .models import Campus
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
