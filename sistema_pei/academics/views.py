# Create your views here.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.http import JsonResponse
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
from sistema_pei.academics import models
from sistema_pei.core import constants
from sistema_pei.core.mixins import ProtectedErrorMessageMixin
from sistema_pei.core.mixins import TitleViewMixin
from sistema_pei.educational_plan.models import Pei
from sistema_pei.people.models import Student
from sistema_pei.people.models import Teacher
from sistema_pei.users.permissions import AssistentOrCoordinatorPermission, CoordinatorPermission


class AcademicsIndexView(
    LoginRequiredMixin,
    AssistentOrCoordinatorPermission,
    TitleViewMixin,
    generic.TemplateView,
):
    template_name = "academics/index.html"
    title = _("Acadêmico")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Components
        context["courses_counter"] = models.Course.objects.count()
        context["subjects_counter"] = models.Subject.objects.count()
        context["offers_counter"] = models.Offer.objects.current_offers().count()
        context["peis_counter"] = Pei.objects.count()

        # Participants
        context["students_counter"] = Student.objects.count()
        context["teachers_counter"] = Teacher.objects.count()

        return context


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


class OfferListView(LoginRequiredMixin, TitleViewMixin, FilterView, generic.ListView):
    title = _("Ofertas")
    paginate_by = constants.DEFAULT_PAGE_SIZE
    filterset_class = filters.OfferFilter
    template_name = "academics/offers/offer_list.html"

    def get_queryset(self):
        queryset = models.Offer.objects.all()
        filter_data = self.request.GET

        if not filter_data or not any(filter_data.values()):
            queryset = models.Offer.objects.current_offers()

        return self.filterset_class(self.request.GET, queryset=queryset).qs


class OfferCreateView(
    SuccessMessageMixin,
    LoginRequiredMixin,
    TitleViewMixin,
    CreateView,
):
    title = _("Criar Oferta")
    model = models.Offer
    form_class = forms.OfferForm
    template_name = "academics/offers/offer_form.html"
    success_message = _("Oferta criada com sucesso!")
    success_url = reverse_lazy("academics:offer_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        messages.error(self.request, "Erro ao criar oferta")
        return redirect(self.request.headers.get("referer", "/"))


class OfferUpdateView(
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
    success_url = reverse_lazy("academics:offer_list")

    def get_object(self, queryset=None):
        return get_object_or_404(models.Offer, id=self.kwargs["pk"])

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "academics:offer_list",
        )


class OfferDetailView(LoginRequiredMixin, FilterView, generic.ListView):
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


class OfferDeleteView(
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
                "Não é possível remover o aluno desta oferta"
                "porque existem PEIs associados.",
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


class RemoveStudentFromSubjectView(View):
    def get(self, request, subject_id, student_id):
        subject = get_object_or_404(models.Subject, id=subject_id)
        student = get_object_or_404(Student, id=student_id)
        subject.students.remove(student)
        return redirect(f"/subjects/edit/{subject.id}")


class SubjectDeleteView(
    LoginRequiredMixin,
    ProtectedErrorMessageMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    model = models.Subject
    success_url = reverse_lazy("academics:subject_list")
    success_message = _("A disciplina foi excluída com sucesso.")
    protected_warning_message = _(
        "Não é possível excluir a disciplina, pois ele possui "
        "uma ou mais ofertas associadas.",
    )


class SubjectsPageView(
    LoginRequiredMixin,
    TitleViewMixin,
    FilterView,
    generic.ListView,
):
    model = models.Subject
    title = _("Disciplinas")
    paginate_by = constants.DEFAULT_PAGE_SIZE
    filterset_class = filters.SubjectFilter
    template_name = "academics/subjects/subject_list.html"
    ordering = ["name"]


class CreateSubjectPageView(
    SuccessMessageMixin,
    LoginRequiredMixin,
    TitleViewMixin,
    CreateView,
):
    title = _("Criar Disciplina")
    model = models.Subject
    form_class = forms.SubjectForm
    template_name = "academics/subjects/subject_form.html"
    success_message = _("Disciplina criada com sucesso!")
    success_url = reverse_lazy("academics:subject_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        messages.error(self.request, "Erro ao criar oferta")
        return redirect(self.request.headers.get("referer", "/"))


class EditSubjectPageView(
    SuccessMessageMixin,
    LoginRequiredMixin,
    TitleViewMixin,
    UpdateView,
):
    title = _("Editar Disciplina")
    model = models.Subject
    form_class = forms.SubjectForm
    success_message = _("A disciplina foi atualizada com sucesso.")
    template_name = "academics/subjects/subject_form.html"
    success_url = reverse_lazy("academics:subject_list")

    def get_object(self, queryset=None):
        return get_object_or_404(models.Subject, id=self.kwargs["pk"])

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class SubjectDetailView(LoginRequiredMixin, TitleViewMixin, generic.DetailView):
    model = models.Subject
    title = _("Detalhes da disciplina")
    template_name = "academics/subjects/subject_detail.html"


class PeiListView(
    LoginRequiredMixin,
    TitleViewMixin,
    FilterView,
    generic.ListView,
):
    model = Pei
    title = _("PEIs")
    paginate_by = constants.DEFAULT_PAGE_SIZE
    filterset_class = filters.PeiFilter
    template_name = "academics/peis/pei_list.html"


class PeiCreateView(
    SuccessMessageMixin,
    LoginRequiredMixin,
    TitleViewMixin,
    CreateView,
):
    title = _("Cadastrar PEI")
    model = Pei
    form_class = forms.PeiForm
    template_name = "academics/peis/pei_form.html"
    success_message = _("PEI criado com sucesso!")
    success_url = reverse_lazy("academics:pei_list")

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
    model = Pei
    form_class = forms.PeiForm
    success_message = _("O PEI foi atualizado com sucesso.")
    template_name = "academics/peis/pei_form.html"
    success_url = reverse_lazy("academics:pei_list")

    def get_object(self, queryset=None):
        return get_object_or_404(Pei, id=self.kwargs["pk"])

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class PeiDeleteView(
    LoginRequiredMixin,
    ProtectedErrorMessageMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    model = Pei
    success_url = reverse_lazy("academics:pei_list")
    success_message = _("O pei foi removido com sucesso.")
    protected_warning_message = _(
        "Não é possível excluir o pei, pois ele possui " "itens associados.",
    )

class PeiDetailView(LoginRequiredMixin, TitleViewMixin, generic.DetailView):
    model = Pei
    title = _("Detalhes do PEI")
    template_name = "academics/peis/pei_detail.html"

class PeiMarkCompletedView(CoordinatorPermission, LoginRequiredMixin, View):
    def get(self, request, pk):
        pei = get_object_or_404(Pei, id=pk)

        pei.status = Pei.StatusChoice.COMPLETED
        pei.save()
        messages.success(request, 'PEI marcado como concluído com sucesso.')

        return redirect('academics:pei_list')
