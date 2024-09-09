# Create your views here.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.db.models import Q
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
from sistema_pei.academics.constants import COURSE_TYPE
from sistema_pei.core import constants
from sistema_pei.core.mixins import TitleViewMixin
from sistema_pei.people.models import Student


class AcademicsIndexView(LoginRequiredMixin, TitleViewMixin, generic.TemplateView):
    template_name = "academics/index.html"
    title = _("Acadêmico")

class CoursesPageView(LoginRequiredMixin, TitleViewMixin, generic.ListView):
    model = models.Course
    title = _("Cursos")
    paginate_by = constants.DEFAULT_PAGE_SIZE
    filterset_class = filters.CourseFilter
    template_name = "academics/course_list.html"


class CreateCoursesPageView(generic.TemplateView):
    template_name = "pages/courses/create-course.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["course_types"] = [course[0] for course in COURSE_TYPE]
        return context

    def post(self, request, *args, **kwargs):
        form = forms.CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("academics:courses")
        return self.render_to_response(self.get_context_data(form=form))

class EditCoursePageView(generic.TemplateView):
    template_name = "pages/courses/edit-course.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs.get("course_id")
        course = get_object_or_404(models.Course, id=course_id)
        course_subjects = course.subjects.all()

        filters = {}
        if "search_subject" in self.request.GET:
            filters["search_subject"] = self.request.GET["search_subject"]
            course_subjects = course_subjects.filter(
                Q(name__icontains=self.request.GET["search_subject"]),
            )

        context["course"] = course
        context["course_subjects"] = course_subjects
        context["course_types"] = [course[0] for course in COURSE_TYPE]

        return context

    def post(self, request, *args, **kwargs):
        course_id = self.kwargs.get("course_id")
        course = get_object_or_404(models.Course, id=course_id)
        form = forms.CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("courses")
        return self.render_to_response(self.get_context_data(form=form))

class DeleteCourseView(View):
    def get(self, request, course_id):
        course = get_object_or_404(models.Course, id=course_id)
        course.delete()
        return redirect("courses")

class OffersPageView(TitleViewMixin, FilterView, generic.ListView):
    title = _("Ofertas")
    paginate_by = constants.DEFAULT_PAGE_SIZE
    filterset_class = filters.OfferFilter
    template_name = "academics/offer_list.html"

    def get_queryset(self):
        # Listar somente ofertas do curso
        course_id = self.kwargs.get("course_id")
        queryset = models.Offer.objects.filter(course_id=course_id)
        filterset = filters.OfferFilter(self.request.GET, queryset=queryset)
        return filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs.get("course_id")
        course = get_object_or_404(models.Course, id=course_id)
        context["course"] = course

        return context


class CreateOfferPageView(TitleViewMixin, CreateView):
    title = _("Criar Oferta")
    model = models.Offer
    form_class = forms.OfferForm

    def form_valid(self, form):
        self.object = form.save()
        form = self.get_form_class()()
        messages.success(self.request, "Oferta criada com sucesso!")
        return redirect(f"/academics/offers/{self.object.course.id}")

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        messages.error(self.request, "Erro ao criar oferta")
        return redirect(self.request.headers.get("referer", "/"))

    def get_success_url(self):
        return self.request.path


class EditOfferPageView(TitleViewMixin, UpdateView):
    title = _("Editar Oferta")
    model = models.Offer
    form_class = forms.OfferForm
    context_object_name = "offer"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isEditing"] = True
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(models.Offer, id=self.kwargs["offer_id"])

    def get_success_url(self):
        return reverse_lazy(
            "academics:offers",
            kwargs={"course_id": self.object.course_id},
        )

    def form_valid(self, form):
        messages.success(self.request, "Oferta editada com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao editar a oferta")
        return super().form_invalid(form)


class OfferDetailsPageView(FilterView, generic.ListView):
    paginate_by = 10
    filterset_class = filters.EnrollmentFilter
    template_name = "academics/offer_detail.html"

    def get_queryset(self):
        offer_id = self.kwargs.get("offer_id")
        offer = get_object_or_404(models.Offer, id=offer_id)
        return offer.enrollments.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        offer_id = self.kwargs.get("offer_id")
        offer = get_object_or_404(models.Offer, id=offer_id)

        course_id = self.kwargs.get("course_id")
        course = get_object_or_404(models.Course, id=course_id)
        context["course"] = course
        context["offer"] = offer

        context["selector_students"] = Student.objects.filter(
            course=offer.course,
        ).exclude(id__in=offer.enrollments.values_list("student_id", flat=True))

        return context


class DeleteOfferView(View):
    def get(self, request, offer_id):
        offer = get_object_or_404(models.Offer, id=offer_id)
        try:
            offer.delete()
            messages.success(request, "Oferta removida com sucesso!")
            return redirect(request.headers.get("referer", "/"))
        except ProtectedError:
            messages.error(
                request,
                "Erro - Você não pode remover ofertas com alunos associados!",
            )
            return redirect(request.headers.get("referer", "/"))


class RemoveStudentFromOfferView(View):
    def get(self, request, offer_id, student_id):
        offer = get_object_or_404(models.Offer, id=offer_id)
        student = get_object_or_404(Student, id=student_id)

        try:
            enrollment = get_object_or_404(models.Enrollment, offer=offer, student=student)
            enrollment.delete()
            messages.success(request, "Aluno removido com sucesso da oferta.")
        except ProtectedError:
            messages.error(
                request,
                "Não é possível remover o aluno desta oferta porque existem PEIs associados.",
            )

        return redirect(f"/academics/offers/details/{student.course.id}/{offer.id}")


class AddStudentToOfferView(View):
    def post(self, request, offer_id):
        offer = get_object_or_404(models.Offer, id=offer_id)
        student_id = request.POST.get("student")
        student = get_object_or_404(Student, id=student_id)

        if not models.Enrollment.objects.filter(offer=offer, student=student).exists():
            models.Enrollment.objects.create(
                offer=offer,
                student=student,
                YearSemesterReference=student.reference_period,
            )

        return redirect(f"/academics/offers/details/{student.course.id}/{offer.id}")
