# Create your views here.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views import generic
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django_filters.views import FilterView

from sistema_pei.academics import filters
from sistema_pei.academics import forms
from sistema_pei.core import constants
from sistema_pei.core.mixins import ProtectedErrorMessageMixin
from sistema_pei.core.mixins import TitleViewMixin
from sistema_pei.educational_plan import models
from sistema_pei.educational_plan.filters import PeiFilter
from sistema_pei.users.permissions import CoordinatorPermission


# Create your views here.
class PeiListView(
    LoginRequiredMixin,
    TitleViewMixin,
    FilterView,
    generic.ListView,
):
    model = models.Pei
    title = _("PEIs")
    paginate_by = constants.DEFAULT_PAGE_SIZE
    filterset_class = PeiFilter
    template_name = "educational_plan/peis/pei_list.html"


class PeiCreateView(
    SuccessMessageMixin,
    LoginRequiredMixin,
    TitleViewMixin,
    CreateView,
):
    title = _("Cadastrar PEI")
    model = models.Pei
    form_class = forms.PeiForm
    template_name = "educational_plan/peis/pei_form.html"
    success_message = _("PEI criado com sucesso!")
    success_url = reverse_lazy("educational_plan:pei_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        messages.error(self.request, "Erro ao criar PEI")
        return redirect(self.request.headers.get("referer", "/"))


class PeiUpdateView(
    SuccessMessageMixin,
    LoginRequiredMixin,
    TitleViewMixin,
    UpdateView,
):
    title = _("Editar PEI")
    model = models.Pei
    form_class = forms.PeiForm
    success_message = _("O PEI foi atualizado com sucesso.")
    template_name = "educational_plan/peis/pei_form.html"
    success_url = reverse_lazy("educational_plan:pei_list")

    def dispatch(self, request, *args, **kwargs):
        # Verificar se o usuário logado é o professor associado ao PEI
        pei = self.get_object()
        if pei.enrollment.offer.teacher.email != request.user.email:
            messages.error(request, 'Você não tem permissão para editar este PEI.')
            return redirect('educational_plan:pei_list')

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(models.Pei, id=self.kwargs["pk"])

    def _update_pei_status(self, instance):
        if instance.pk:
            # Se marcado como concluído pelo coordenador, não faz nada
            if instance.status == models.Pei.StatusChoice.COMPLETED:
                return

            fields_to_check = [
                instance.objective,
                instance.adapted_objective,
                instance.content,
                instance.adapted_content,
                instance.methodology,
                instance.adapted_methodology,
                instance.resources,
                instance.adapted_resources,
                instance.assessments,
                instance.adapted_assessments
            ]

            filled_fields = [field for field in fields_to_check if field]

            if len(filled_fields) == len(fields_to_check):
                instance.status = models.Pei.StatusChoice.FEEDBACK
            elif len(filled_fields) > 0:
                instance.status = models.Pei.StatusChoice.IN_PROGRESS
            else:
                instance.status = models.Pei.StatusChoice.NOT_START

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        self._update_pei_status(form.instance)
        return super().form_valid(form)

class PeiDeleteView(
    LoginRequiredMixin,
    ProtectedErrorMessageMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    model = models.Pei
    success_url = reverse_lazy("educational_plan:pei_list")
    success_message = _("O pei foi removido com sucesso.")
    protected_warning_message = _(
        "Não é possível excluir o pei, pois ele possui " "itens associados.",
    )

    def dispatch(self, request, *args, **kwargs):
        # Verificar se o usuário logado é o professor associado ao PEI
        pei = self.get_object()
        if pei.enrollment.offer.teacher.email != request.user.email:
            messages.error(request, 'Você não tem permissão para deletar este PEI.')
            return redirect('educational_plan:pei_list')

        return super().dispatch(request, *args, **kwargs)

class PeiDetailView(LoginRequiredMixin, TitleViewMixin, generic.DetailView):
    model = models.Pei
    title = _("Detalhes do PEI")
    template_name = "educational_plan/peis/pei_detail.html"

class PeiMarkCompletedView(CoordinatorPermission, LoginRequiredMixin, View):
    def get(self, request, pk):
        pei = get_object_or_404(models.Pei, id=pk)

        pei.status = models.Pei.StatusChoice.COMPLETED
        pei.save()
        messages.success(request, 'PEI marcado como concluído com sucesso.')

        return redirect('educational_plan:pei_list')
