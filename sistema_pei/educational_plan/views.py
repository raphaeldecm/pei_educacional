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
from django.views.generic import DetailView
from django.http import HttpResponse
from sistema_pei.educational_plan.forms import CommentForm, PeiForm
from sistema_pei.educational_plan.services import generatePeiExportHtml
from xhtml2pdf import pisa
from django.views.generic import View
from sistema_pei.educational_plan.models import Comment
from .models import Pei

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

    def get_queryset(self):
        queryset = models.Pei.objects.all()
        filter_data = self.request.GET

        if not filter_data or not any(filter_data.values()):
            queryset = models.Pei.objects.current_peis()

        return self.filterset_class(self.request.GET, queryset=queryset).qs


class PeiCreateView(
    SuccessMessageMixin,
    LoginRequiredMixin,
    TitleViewMixin,
    CreateView,
):
    title = _("Cadastrar PEI")
    model = models.Pei
    form_class = PeiForm
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
    form_class = PeiForm
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

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(pei=self.object).order_by('-date')
        return context


class PeiMarkCompletedView(CoordinatorPermission, LoginRequiredMixin, View):
    def get(self, request, pk):
        pei = get_object_or_404(models.Pei, id=pk)

        pei.status = models.Pei.StatusChoice.COMPLETED
        pei.save()
        messages.success(request, 'PEI marcado como concluído com sucesso.')

        return redirect('educational_plan:pei_list')


class PeiExportPdfView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pei_id = kwargs.get('pk')
        html = generatePeiExportHtml(pei_id)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="pei_{pei_id}.pdf"'

        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('Erro ao gerar o PDF', status=500)

        return response

class PeiExportPreviewView(LoginRequiredMixin, DetailView):
    model = Pei
    template_name = 'educational_plan/peis/pei_export.html'
    context_object_name = 'pei'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pei = Pei.objects.get(pk=self.kwargs['pk'])
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.pei = pei
            comment.updated_by = self.request.user
            comment.created_by = self.request.user
            comment.save()
            messages.success(request, 'Comentário adicionado com sucesso.')
        else:
            print(form.errors)
            messages.success(request, 'Erro ao adicionar comentário.')
        return redirect('educational_plan:pei_detail', pk=pei.pk)

class CommentDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])

        if (comment.created_by == request.user):
            comment.delete()
            messages.success(request, 'Comentário removido com sucesso.')
        else:
            messages.error(request, 'Você não tem permissão para remover este comentário.')

        return redirect('educational_plan:pei_detail', pk=comment.pei.pk)
