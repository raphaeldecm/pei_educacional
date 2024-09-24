import django_filters
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label="Nome")
    email = django_filters.CharFilter(lookup_expr="icontains", label="Email")
    sector = django_filters.ChoiceFilter(choices=User.Sector.choices, label="Setor")
    groups = django_filters.ModelChoiceFilter(
        queryset=Group.objects.all(),
        label="Grupo",
    )

    class Meta:
        model = User
        fields = ["name", "email", "sector", "groups"]
