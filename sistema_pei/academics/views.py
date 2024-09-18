# Create your views here.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views import generic
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django_filters.views import FilterView

from sistema_pei.academics import filters
from sistema_pei.academics import forms
from sistema_pei.academics import models
from sistema_pei.core import constants
from sistema_pei.core.mixins import ProtectedErrorMessageMixin
from sistema_pei.core.mixins import TitleViewMixin
from sistema_pei.people.models import Student


class AcademicsIndexView(LoginRequiredMixin, TitleViewMixin, generic.TemplateView):
    template_name = "academics/index.html"
    title = _("Acadêmico")


class CourseListView(LoginRequiredMixin, TitleViewMixin, FilterView, generic.ListView):
    model = models.Course
    title = _("Cursos")
    paginate_by = constants.DEFAULT_PAGE_SIZE
    filterset_class = filters.CourseFilter
    template_name = "academics/course/course_list.html"
    ordering = ["name"]


class CourseCreateView(
    LoginRequiredMixin,
    TitleViewMixin,
    SuccessMessageMixin,
    generic.CreateView,
):
    model = models.Course
    form_class = forms.CourseForm
    title = _("Criar Curso")
    template_name = "academics/course/course_form.html"
    success_url = reverse_lazy("academics:course_list")
    success_message = _("O curso foi cadastrado com sucesso.")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class CourseUpdateView(
    LoginRequiredMixin,
    TitleViewMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    model = models.Course
    form_class = forms.CourseForm
    title = _("Editar Curso")
    template_name = "academics/course/course_form.html"
    success_url = reverse_lazy("academics:course_list")
    success_message = _("O curso foi atualizado com sucesso.")


class CourseDetailView(LoginRequiredMixin, TitleViewMixin, generic.DetailView):
    model = models.Course
    context_object_name = "course"
    title = _("Detalhes do Curso")
    template_name = "academics/course/course_detail.html"


class CourseDeleteView(
    LoginRequiredMixin,
    ProtectedErrorMessageMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    model = models.Course
    success_url = reverse_lazy("academics:course_list")
    success_message = _("O curso foi excluído com sucesso.")
    protected_warning_message = _(
        "Não é possível excluir o curso, pois ele possui"
        "uma ou mais disciplinas associadas.",
    )


class OffersPageView(LoginRequiredMixin, TitleViewMixin, FilterView, generic.ListView):
    title = _("Ofertas")
    paginate_by = constants.DEFAULT_PAGE_SIZE
    filterset_class = filters.OfferFilter
    template_name = "academics/offers/offer_list.html"

    def get_queryset(self):
        queryset = models.Offer.objects.all()
        filter_data = self.request.GET

        if not filter_data or not any(filter_data.values()):
            queryset = queryset.filter(
                year=now().year,
                semester="1" if now().month <= 6 else "2",
            )

        return self.filterset_class(self.request.GET, queryset=queryset).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_data = self.request.GET

        if not filter_data or not any(filter_data.values()):
            context["default_year"] = now().year
            context["default_semester"] = "1" if now().month <= 6 else "2"

        return context


class CreateOfferPageView(LoginRequiredMixin, TitleViewMixin, CreateView):
    title = _("Criar Oferta")
    model = models.Offer
    form_class = forms.OfferForm
    template_name = "academics/offers/offer_form.html"

    def form_valid(self, form):
        self.object = form.save()
        form = self.get_form_class()()
        messages.success(self.request, "Oferta criada com sucesso!")
        return redirect("/academics/offers/list/")

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        messages.error(self.request, "Erro ao criar oferta")
        return redirect(self.request.headers.get("referer", "/"))

    def get_success_url(self):
        return self.request.path


class EditOfferPageView(
    SuccessMessageMixin,
    LoginRequiredMixin,
    TitleViewMixin,
    UpdateView,
):
    title = _("Editar Oferta")
    model = models.Offer
    form_class = forms.OfferForm
    success_message = _("A oferta foi atualizada com sucesso.")
    template_name = "academics/offers/offer_form.html"
    context_object_name = "offer"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isEditing"] = True
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(models.Offer, id=self.kwargs["pk"])

    def get_success_url(self):
        return reverse_lazy(
            "academics:offer_list",
        )


class OfferDetailsPageView(LoginRequiredMixin, FilterView, generic.ListView):
    paginate_by = 10
    filterset_class = filters.EnrollmentFilter
    template_name = "academics/offers/offer_detail.html"

    def get_queryset(self):
        offer_id = self.kwargs.get("pk")
        offer = get_object_or_404(models.Offer, id=offer_id)
        return offer.enrollments.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        offer_id = self.kwargs.get("pk")
        offer = get_object_or_404(models.Offer, id=offer_id)

        context["offer"] = offer

        context["selector_students"] = Student.objects.filter(
            course=offer.course,
        ).exclude(id__in=offer.enrollments.values_list("student_id", flat=True))

        return context


class DeleteOfferView(
    LoginRequiredMixin,
    ProtectedErrorMessageMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    model = models.Offer
    success_url = reverse_lazy("academics:offer_list")
    success_message = _("A oferta foi excluída com sucesso.")
    protected_warning_message = _(
        "Não é possível excluir a oferta, pois ele possui"
        "um ou mais alunos associados.",
    )


class RemoveStudentFromOfferView(SuccessMessageMixin, LoginRequiredMixin, View):
    def post(self, request, offer_id, student_id):
        offer = get_object_or_404(models.Offer, id=offer_id)
        student = get_object_or_404(Student, id=student_id)

        try:
            enrollment = get_object_or_404(
                models.Enrollment,
                offer=offer,
                student=student,
            )
            enrollment.delete()
            messages.success(request, "Aluno removido com sucesso da oferta.")
        except ProtectedError:
            messages.error(
                request,
                "Não é possível remover o aluno desta oferta porque existem PEIs associados.",
            )

        return redirect(f"/academics/offers/detail/{offer.id}/")


class AddStudentToOfferView(LoginRequiredMixin, View):
    def post(self, request, pk):
        offer = get_object_or_404(models.Offer, id=pk)
        student_id = request.POST.get("student")
        student = get_object_or_404(Student, id=student_id)

        if not models.Enrollment.objects.filter(offer=offer, student=student).exists():
            models.Enrollment.objects.create(
                offer=offer,
                student=student,
                YearSemesterReference=student.reference_period,
            )

        return redirect(f"/academics/offers/detail/{offer.id}/")


class GetSubjectsByCourseView(LoginRequiredMixin, View):
    def get(self, request, pk):
        subjects = models.Subject.objects.filter(courses=pk)
        subjects_data = list(subjects.values("id", "name"))
        return JsonResponse({"subjects": subjects_data})
