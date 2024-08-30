# Create your views here.
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.views.generic.edit import CreateView
from django.core.paginator import PageNotAnInteger
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views import View
from django.core.paginator import EmptyPage
from sistema_pei.academics import constants
from sistema_pei.academics.filters import OfferFilter
from sistema_pei.academics.forms import OfferForm
from sistema_pei.academics.models import Course, Enrollment, Offer, Subject
from django.views.generic import TemplateView
from django.views import generic
from django.db.models import ProtectedError
from django.db.models import Q

from sistema_pei.people.models import Student, Teacher


class OffersPageView(FilterView, generic.ListView):
    model = Offer
    template_name = "offers/offers.html"
    paginate_by = constants.DEFAULT_PAGE_SIZE
    filterset_class = OfferFilter

    def get_queryset(self):
        #Listar somente ofertas do curso
        course_id = self.kwargs.get('course_id')
        queryset = Offer.objects.filter(course_id=course_id)
        filterset = OfferFilter(self.request.GET, queryset=queryset)
        return filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs.get("course_id")
        course = get_object_or_404(Course, id=course_id)
        context["course"] = course

        # Breadcrumbs
        context["breadcrumbs_data"] = [
            {
                "icon": "images/icons/icon-home-green.svg",
                "name": "Home",
                "url": "home",
            },
            {
                "icon": "images/icons/icon-courses-green.svg",
                "name": "Cursos",
                "url": "courses",
            },
            {
                "icon": "images/icons/icon-courses-green.svg",
                "name": "Matérias",
            },
            {
                "icon": "images/icons/highlighter-green.svg",
                "name": f"Ofertas de {course.name}",
            },
        ]

        return context
class CreateOfferPageView(CreateView):
    template_name = "offers/create-offer.html"
    form_class = OfferForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Breadcrumbs
        context["breadcrumbs_data"] = [
            {
                "icon": "images/icons/icon-home-green.svg",
                "name": "Home",
                "url": "home",
            },
            {
                "icon": "images/icons/highlighter-green.svg",
                "name": "Oferta",
            },
            {
                "icon": "images/icons/icon-edit-green.svg",
                "name": "Criar Oferta",
            },
        ]

        return context

    def form_valid(self, form):
        self.object = form.save()
        form = self.get_form_class()()
        messages.success(self.request, "Oferta criada com sucesso!")
        return redirect(self.request.META.get('HTTP_REFERER', '/'))

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        messages.error(self.request, "Erro ao criar oferta")
        return redirect(self.request.META.get('HTTP_REFERER', '/'))

    def get_success_url(self):
        return self.request.path
      
class EditOfferPageView(TemplateView):
    template_name = "offers/edit-offer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offer_id = self.kwargs.get("offer_id")
        offer = get_object_or_404(Offer, id=offer_id)

        # Breadcrumbs
        context["breadcrumbs_data"] = [
            {
                "icon": "images/icons/icon-home-green.svg",
                "name": "Home",
                "url": "home",
            },
            {
                "icon": "images/icons/highlighter-green.svg",
                "name": "Ofertas",
            },
            {
                "icon": "images/icons/icon-edit-green.svg",
                "name": "Editar Oferta",
            },
        ]

        context["offer"] = offer
        context["selector_teachers"] = Teacher.objects.all()
        context["selector_subjects"] = Subject.objects.all()

        return context

    def post(self, request, *args, **kwargs):
        offer_id = self.kwargs.get("offer_id")
        offer = get_object_or_404(Offer, id=offer_id)
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
        return self.render_to_response(self.get_context_data(form=form))
      
class OfferDetailsPageView(TemplateView):
    template_name = "offers/offer-details.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        offer_id = self.kwargs.get("offer_id")
        offer = get_object_or_404(Offer, id=offer_id)
        
        course_id = self.kwargs.get("course_id")
        course = get_object_or_404(Course, id=course_id)
        context["course"] = course

        # Breadcrumbs
        context["breadcrumbs_data"] = [
            {
                "icon": "images/icons/icon-home-green.svg",
                "name": "Home",
                "url": "home",
            },
            {
                "icon": "images/icons/highlighter-green.svg",
                "name": "Ofertas",
            },
            {
                "icon": "images/icons/highlighter-green.svg",
                "name": offer.subject.name,
            },
        ]

        enrolments = offer.enrollments.all()

        if "search" in self.request.GET:
            enrolments = enrolments.filter(
                Q(student__name__icontains=self.request.GET["search"]),
            )

        context["offer"] = offer


        paginator = Paginator(enrolments, self.paginate_by)
        page_number = self.request.GET.get("page")

        try:
            enrolments = paginator.page(page_number)
        except PageNotAnInteger:
            enrolments = paginator.page(1)
        except EmptyPage:
            enrolments = paginator.page(paginator.num_pages)

        context["enrollments"] = enrolments

        context["selector_students"] = Student.objects.filter(course=offer.course).exclude(id__in=offer.enrollments.values_list('student_id', flat=True))
      

        return context
      
class DeleteOfferView(View):
    def get(self, request, offer_id):
        offer = get_object_or_404(Offer, id=offer_id)
        try:
            offer.delete()
            messages.success(request, "Oferta removida com sucesso!")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        except ProtectedError:
            messages.error(
                request,
                "Erro - Você não pode remover ofertas com alunos associados!",
            )
            return redirect(request.META.get('HTTP_REFERER', '/'))
          
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
                "Não é possível remover o aluno desta oferta porque existem PEIs associados."
            )
        
        return redirect(f"/offers/details/{student.course.id}/{offer.id}")