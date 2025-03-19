from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django_filters.views import FilterView

from sistema_pei.core import constants
from sistema_pei.educational_plan.filters import PeiFilter
from sistema_pei.educational_plan.models import Pei
from sistema_pei.users.permissions import AnyGroupPermission


class HomeListView(
    AnyGroupPermission,
    LoginRequiredMixin,
    FilterView,
    generic.ListView,
):
    model = Pei
    paginate_by = constants.DEFAULT_PAGE_SIZE
    filterset_class = PeiFilter
    template_name = "home.html"

    def get_queryset(self):
        queryset = Pei.objects.all()
        filter_data = self.request.GET

        # Filtro por semestre e ano atuais
        if not filter_data or not any(filter_data.values()):
            queryset = Pei.objects.current_peis()

        # Filtro por professor logado
        if self.request.user.groups.filter(name="Teacher").exists():
            if not filter_data or not any(filter_data.values()):
                queryset = Pei.objects.filter(
                    enrollment__offer__teachers__email=self.request.user.email,
                )

        return self.filterset_class(
            self.request.GET, queryset=queryset, request=self.request
        ).qs

    # Cards
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = Pei.objects.all()

        if self.request.user.groups.filter(name="Teacher").exists():
            queryset = Pei.objects.filter(
                enrollment__offer__teachers__email=self.request.user.email
            )

        context["pending_peis"] = queryset.filter(status="NOT_START").count()
        context["in_progress_peis"] = queryset.filter(status="IN_PROGRESS").count()
        context["filled_peis"] = queryset.filter(status="FEEDBACK").count()
        context["finished_peis"] = queryset.filter(status="COMPLETED").count()

        return context
