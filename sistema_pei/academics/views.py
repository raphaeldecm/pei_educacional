# Create your views here.
from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views import generic
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django_filters.views import FilterView

from sistema_pei.core import constants
from sistema_pei.academics.filters import EnrollmentFilter
from sistema_pei.academics.filters import OfferFilter
from sistema_pei.academics.forms import OfferForm
from sistema_pei.academics.models import Course
from sistema_pei.academics.models import Enrollment
from sistema_pei.academics.models import Offer
from sistema_pei.people.models import Student


class OffersPageView(FilterView, generic.ListView):
    paginate_by = constants.DEFAULT_PAGE_SIZE
    filterset_class = OfferFilter
    template_name = "academics/offer_list.html"

    def get_queryset(self):
        # Listar somente ofertas do curso
        course_id = self.kwargs.get("course_id")
        queryset = Offer.objects.filter(course_id=course_id)
        filterset = OfferFilter(self.request.GET, queryset=queryset)
        return filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs.get("course_id")
        course = get_object_or_404(Course, id=course_id)
        context["course"] = course

        return context


class CreateOfferPageView(CreateView):
    model = Offer
    form_class = OfferForm

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


class EditOfferPageView(UpdateView):
    model = Offer
    form_class = OfferForm
    context_object_name = "offer"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isEditing"] = True
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Offer, id=self.kwargs["offer_id"])

    def get_success_url(self):
        return reverse_lazy(
            "academics:offers", kwargs={"course_id": self.object.course_id}
        )

    def form_valid(self, form):
        messages.success(self.request, "Oferta editada com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao editar a oferta")
        return super().form_invalid(form)


class OfferDetailsPageView(FilterView, generic.ListView):
    paginate_by = 10
    filterset_class = EnrollmentFilter
    template_name = "academics/offer_detail.html"

    def get_queryset(self):
        offer_id = self.kwargs.get("offer_id")
        offer = get_object_or_404(Offer, id=offer_id)
        return offer.enrollments.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        offer_id = self.kwargs.get("offer_id")
        offer = get_object_or_404(Offer, id=offer_id)

        course_id = self.kwargs.get("course_id")
        course = get_object_or_404(Course, id=course_id)
        context["course"] = course
        context["offer"] = offer

        context["selector_students"] = Student.objects.filter(
            course=offer.course
        ).exclude(id__in=offer.enrollments.values_list("student_id", flat=True))

        return context


class DeleteOfferView(View):
    def get(self, request, offer_id):
        offer = get_object_or_404(Offer, id=offer_id)
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
        offer = get_object_or_404(Offer, id=offer_id)
        student = get_object_or_404(Student, id=student_id)

        try:
            enrollment = get_object_or_404(Enrollment, offer=offer, student=student)
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
        offer = get_object_or_404(Offer, id=offer_id)
        student_id = request.POST.get("student")
        student = get_object_or_404(Student, id=student_id)

        if not Enrollment.objects.filter(offer=offer, student=student).exists():
            Enrollment.objects.create(
                offer=offer,
                student=student,
                YearSemesterReference=student.reference_period,
            )

        return redirect(f"/academics/offers/details/{student.course.id}/{offer.id}")
