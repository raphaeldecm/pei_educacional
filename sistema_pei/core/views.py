import datetime
import re

from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Count
from django.db.models import ProtectedError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import TemplateView
from django.views.generic import View

from sistema_pei.academics.constants import COURSE_TYPE
from sistema_pei.academics.models import Course
from sistema_pei.academics.models import Enrollment
from sistema_pei.academics.models import Offer
from sistema_pei.academics.models import Subject
from sistema_pei.core.forms import CourseForm
from sistema_pei.core.forms import EnrollmentForm
from sistema_pei.core.forms import OfferForm
from sistema_pei.core.forms import SubjectForm
from sistema_pei.educational_plan.models import Pei
from sistema_pei.people.forms import StudentFilesForm
from sistema_pei.people.forms import ViewEditDataStudentForm
from sistema_pei.people.forms import ViewEdithistoricStudentForm
from sistema_pei.people.models import Student
from sistema_pei.people.models import StudentFile
from sistema_pei.people.models import Teacher
from sistema_pei.people.models import User
from sistema_pei.users.models import Sector


class HomePageView(TemplateView):
    template_name = "pages/home.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filter Selectors
        context["selector_courses"] = Course.objects.all()
        context["selector_teachers"] = Teacher.objects.all()
        context["selector_offers"] = Subject.objects.all()

        # Cards
        context["pending_peis"] = Pei.objects.filter(status="NOT_START").count()
        context["in_progress_peis"] = Pei.objects.filter(status="IN_PROGRESS").count()
        context["filled_peis"] = Pei.objects.filter(status="FEEDBACK").count()
        context["finished_peis"] = Pei.objects.filter(status="COMPLETED").count()

        filters = {}

        if "course" in self.request.GET:
            filters["enrollment__student__course__id"] = self.request.GET["course"]
        if "teacher" in self.request.GET:
            filters["enrollment__offer__teacher__id"] = self.request.GET["teacher"]
        if "period" in self.request.GET:
            filters["enrollment__student__course__period"] = self.request.GET["period"]
        if "status" in self.request.GET:
            filters["status"] = self.request.GET["status"]
        if "subject" in self.request.GET:
            filters["enrollment__offer__subject__id"] = self.request.GET["subject"]

        peis_list = Pei.objects.filter(**filters).annotate(
            subject_count=Count("enrollment__student__course__subjects", distinct=True),
        )

        if "search" in self.request.GET:
            peis_list = peis_list.filter(
                Q(enrollment__student__name__icontains=self.request.GET["search"])
                | Q(
                    enrollment__student__registration__icontains=self.request.GET[
                        "search"
                    ],
                ),
            )

        paginator = Paginator(peis_list, self.paginate_by)
        page_number = self.request.GET.get("page")

        try:
            all_peis = paginator.page(page_number)
        except PageNotAnInteger:
            all_peis = paginator.page(1)

        context["all_peis"] = all_peis

        return context


class UsersPageView(TemplateView):
    template_name = "pages/users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = Group.objects.all()
        context["sectors"] = Sector.objects.all()

        request = self.request
        if request.GET.get("alert") == "success":
            messages.success(request, "Convite enviado!")
        elif request.GET.get("alert") == "error":
            messages.error(request, "Usuário já cadastrado!")

        return context

    def post(self, request, *args, **kwargs):
        recipient = request.POST.get("recipient")
        username = re.split(r"@", recipient)[0]

        sector = Sector.objects.get(id=request.POST.get("sector"))
        group = Group.objects.get(id=request.POST.get("group"))
        current_site = get_current_site(request)

        try:
            user = User.objects.create_user(
                email=recipient,
                name=username,
                is_active=False,
                sector=sector,
            )
            group.user_set.add(user)
            EmailAddress.objects.create(
                user=user,
                email=recipient,
                verified=True,
                primary=True,
            )
        except IntegrityError:
            messages.error(request, "Usuário já cadastrado!")
            return redirect("users")

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = f"http://{current_site.domain}/activate/{uid}/{token}/"

        context = {
            "sector_name": sector.name,
            "group_name": group.name,
            "user": username,
            "activation_link": activation_link,
        }

        html_message = render_to_string("layouts/email_template.html", context)

        email = EmailMessage(
            subject="PEIs - Convite",
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
        )

        email.content_subtype = "html"

        try:
            email.send()
            messages.success(request, "Convite enviado!")
        except Exception as e:
            return HttpResponse(f"Erro ao enviar o e-mail: {e}")


class ProfilePageView(TemplateView):
    template_name = "pages/profile.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs.get("student_id")
        student = get_object_or_404(Student, id=student_id)

        # Profile data
        context["student"] = student
        context["student_files"] = StudentFile.objects.filter(student=student)

        # Tabs
        allowed_tabs = ("general", "historic", "grades", "edit_student_data")
        requested_tab = self.request.GET.get("tab", "general")
        if requested_tab in allowed_tabs:
            context["active_tab"] = requested_tab
        else:
            context["active_tab"] = "general"

        sub_tab = self.request.GET.get("sub_tab", "edit_personal_data")
        context["sub_active_tab"] = sub_tab

        ##^ Tab General
        student_peis = context["student_peis"] = Pei.objects.filter(
            enrollment__student=student,
        )

        ### Filters Selectors
        context["selector_teachers"] = Teacher.objects.all()

        ### Filters
        filters = {}
        if "course" in self.request.GET:
            filters["enrollment__offer__subject__courses__id"] = self.request.GET[
                "course"
            ]
        if "teacher" in self.request.GET:
            filters["enrollment__offer__teacher__id"] = self.request.GET["teacher"]
        if "period" in self.request.GET:
            filters["enrollment__offer__subject__courses__period"] = self.request.GET[
                "period"
            ]
        if "status" in self.request.GET:
            filters["status"] = self.request.GET["status"]

        student_peis = student_peis.filter(**filters)

        if "search" in self.request.GET:
            student_peis = student_peis.filter(
                Q(
                    enrollment__offer__subject__name__icontains=self.request.GET[
                        "search"
                    ],
                ),
            )

        student_peis = student_peis.order_by("id")
        paginator = Paginator(student_peis, self.paginate_by)
        page_number = self.request.GET.get("page")

        try:
            student_peis = paginator.page(page_number)
        except PageNotAnInteger:
            student_peis = paginator.page(1)

        context["student_peis"] = student_peis

        ##^ Tab Notes
        student_notes = Enrollment.objects.filter(student=student)
        if "selectedPeriod" in self.request.GET:
            student_notes = student_notes.filter(
                YearSemesterReference=self.request.GET["selectedPeriod"],
            )

        context["student_notes"] = student_notes

        ##^ Tab Edit
        if requested_tab == "edit_student_data":
            if sub_tab == "edit_personal_data":
                form = ViewEditDataStudentForm(instance=student)
                if "form_errors" in self.request.session:
                    form.errors.update(self.request.session["form_errors"])
                    del self.request.session["form_errors"]
                context["form"] = form
            elif sub_tab == "edit_historic":
                form = ViewEdithistoricStudentForm(instance=student)
                if "form_errors" in self.request.session:
                    form.errors.update(self.request.session["form_errors"])
                    del self.request.session["form_errors"]
                context["form"] = form
            elif sub_tab == "edit_files" or sub_tab == "edit_notes":
                form = StudentFilesForm()
                if "form_errors" in self.request.session:
                    form.errors.update(self.request.session["form_errors"])
                    del self.request.session["form_errors"]
                context["form"] = form

        # Sub tab Anexos
        if requested_tab == "edit_student_data":
            if sub_tab == "edit_files":
                context["student_files"] = StudentFile.objects.filter(student=student)

        # Breadcrumbs
        context["breadcrumbs_data"] = [
            {
                "icon": "images/icons/icon-home-green.svg",
                "name": "Home",
                "url": "home",
            },
            {
                "icon": "images/icons/icon-courses-green.svg",
                "name": student.name,
            },
        ]

        return context


class UpdateStudentGradesView(View):
    """
    View para editar as notas de um Enrollment específico.
    """

    def post(self, request, *args, **kwargs):
        enrollment_id = kwargs.get("enrollment_id")
        enrollment = get_object_or_404(Enrollment, id=enrollment_id)

        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            selected_period = request.POST.get("selectedPeriod", 1)
            messages.success(request, "Dados da disciplina atualizados!")
            return redirect(
                f"/profile/{enrollment.student.id}?tab=edit_student_data&sub_tab=edit_notes&selectedPeriod={selected_period}",
            )
        else:
            messages.error(
                request,
                "Erro ao atualizar dados. Verifique os valores inseridos.",
            )
            return redirect(request.headers.get("referer"))


class EditPersonalDataView(View):
    """
    View para editar os dados pessoais de um aluno.
    """

    def post(self, request, *args, **kwargs):
        student_id = kwargs.get("student_id")
        student = get_object_or_404(Student, id=student_id)
        form = ViewEditDataStudentForm(request.POST, request.FILES, instance=student)

        if form.is_valid():
            form.save()
            success_message = "Atulizações salvas com sucesso!"
            messages.success(self.request, success_message)
        else:
            success_message = "Erro ao atualizar dados!"
            messages.error(self.request, success_message)
            request.session["form_errors"] = form.errors
            request.session["form_data"] = request.POST

        return redirect(
            f"/profile/{student.id}?tab=edit_student_data&sub_tab=edit_personal_data#tab",
        )


class EditHistoricPersonalDataView(View):
    """
    View para editar o histórico pessoal de um aluno.
    """

    def post(self, request, *args, **kwargs):
        student_id = kwargs.get("student_id")
        student = get_object_or_404(Student, id=student_id)
        form = ViewEdithistoricStudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            success_message = "Atulizações salvas com sucesso!"
            messages.success(self.request, success_message)
        else:
            success_message = "Erro ao atualizar dados!"
            messages.error(self.request, success_message)
            request.session["form_errors"] = form.errors
            request.session["form_data"] = request.POST

        return redirect(
            f"/profile/{student.id}?tab=edit_student_data&sub_tab=edit_historic#tab",
        )


class DeletePersonalFilesView(View):
    """
    View para deletar arquivos pessoais de um aluno.
    """

    def post(self, request, *args, **kwargs):
        student_id = kwargs.get("student_id")
        file_id = request.POST.get("file_id")
        student = get_object_or_404(Student, id=student_id)
        file = get_object_or_404(StudentFile, id=file_id, student=student)

        try:
            file.delete()
            success_message = "Arquivo deletado com sucesso!"
            messages.success(self.request, success_message)
        except Exception as e:
            error_message = f"Erro ao deletar arquivo: {e!s}"
            messages.error(self.request, error_message)

        return redirect(
            f"/profile/{student.id}?tab=edit_student_data&sub_tab=edit_files#tab",
        )


class UploadStudentFilesView(View):
    """
    View para fazer upload de arquivos para um aluno.
    """

    def post(self, request, *args, **kwargs):
        student_id = kwargs.get("student_id")
        student = get_object_or_404(Student, id=student_id)
        form = StudentFilesForm(request.POST, request.FILES)

        if form.is_valid():
            files = form.cleaned_data["files"]
            for file in files:
                StudentFile.objects.create(student=student, file=file)
            messages.success(request, "Arquivos carregados com sucesso!")
        else:
            messages.error(request, "Erro ao carregar arquivos!")
            request.session["form_errors"] = form.errors
            request.session["form_data"] = request.POST

        return redirect(
            f"/profile/{student.id}?tab=edit_student_data&sub_tab=edit_files#tab",
        )


class CoursesPageView(TemplateView):
    template_name = "pages/courses/courses.html"
    paginate_by = 10

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
                "icon": "images/icons/icon-courses-green.svg",
                "name": "Cursos",
            },
        ]

        # Filter Selectors
        context["course_types"] = [course[0] for course in COURSE_TYPE]

        # Table
        filters = {}
        if "period" in self.request.GET:
            filters["period"] = self.request.GET["period"]
        if "type" in self.request.GET:
            filters["course_type"] = self.request.GET["type"]

        courses_list = Course.objects.filter(**filters)

        if "search" in self.request.GET:
            courses_list = courses_list.filter(
                Q(name__icontains=self.request.GET["search"]),
            )

        courses_list = courses_list.annotate(num_subjects=Count("subjects")).order_by(
            "id",
        )
        paginator = Paginator(courses_list, self.paginate_by)
        page_number = self.request.GET.get("page")

        try:
            all_courses = paginator.page(page_number)
        except PageNotAnInteger:
            all_courses = paginator.page(1)
        except EmptyPage:
            all_courses = paginator.page(paginator.num_pages)

        context["courses"] = all_courses

        return context


class CreateCoursesPageView(TemplateView):
    template_name = "pages/courses/create-course.html"

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
                "icon": "images/icons/icon-courses-green.svg",
                "name": "Cursos",
                "url": "courses",
            },
            {
                "icon": "images/icons/icon-edit-green.svg",
                "name": "Criar Curso",
            },
        ]

        context["course_types"] = [course[0] for course in COURSE_TYPE]
        return context

    def post(self, request, *args, **kwargs):
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("courses")
        return self.render_to_response(self.get_context_data(form=form))


class DeleteCourseView(View):
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        course.delete()
        return redirect("courses")


class RemoveStudentFromSubjectView(View):
    def get(self, request, subject_id, student_id):
        subject = get_object_or_404(Subject, id=subject_id)
        student = get_object_or_404(Student, id=student_id)
        subject.students.remove(student)
        return redirect(f"/subjects/edit/{subject.id}")
    
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
        
        return redirect(f"/offers/details/{offer.id}")

class EditCoursePageView(TemplateView):
    template_name = "pages/courses/edit-course.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs.get("course_id")
        course = get_object_or_404(Course, id=course_id)
        course_subjects = course.subjects.all()

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
                "icon": "images/icons/icon-edit-green.svg",
                "name": "Editar Curso",
            },
        ]

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
        course = get_object_or_404(Course, id=course_id)
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("courses")
        return self.render_to_response(self.get_context_data(form=form))


class DeleteSubjectView(View):
    def get(self, request, subject_id):
        subject = get_object_or_404(Subject, id=subject_id)
        try:
            subject.delete()
            return redirect("courses")
        except ProtectedError:
            return redirect(f"/subjects/edit/{subject.id}?error=protected")


class SubjectsPageView(TemplateView):
    template_name = "pages/subjects/subjects.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs.get("course_id")
        course = get_object_or_404(Course, id=course_id)
        course_subjects = course.subjects.all()
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
        ]

        # Table
        filters = {}
        if "duration" in self.request.GET:
            filters["subject_type"] = self.request.GET["duration"]

        course_subjects = course_subjects.filter(**filters)

        if "search" in self.request.GET:
            course_subjects = course_subjects.filter(
                Q(name__icontains=self.request.GET["search"]),
            )

        paginator = Paginator(course_subjects, self.paginate_by)
        page_number = self.request.GET.get("page")

        try:
            all_course_subjects = paginator.page(page_number)
        except PageNotAnInteger:
            all_course_subjects = paginator.page(1)
        except EmptyPage:
            all_course_subjects = paginator.page(paginator.num_pages)

        context["course_subjects"] = all_course_subjects

        return context


class CreateSubjectPageView(TemplateView):
    template_name = "pages/subjects/create-subject.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs.get("course_id")
        course = get_object_or_404(Course, id=course_id)
        context["current_course"] = course

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
                "icon": "images/icons/icon-edit-green.svg",
                "name": "Criar Matéria",
            },
        ]
        context["course_types"] = [course[0] for course in COURSE_TYPE]
        context["courses"] = Course.objects.all()

        request = self.request
        if request.GET.get("alert") == "error":
            messages.error(request, "Erro - Matéria já foi cadastrada!")

        return context

    def post(self, request, *args, **kwargs):
        form = SubjectForm(request.POST)
        course_id = self.kwargs.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        if form.is_valid():
            existing_subject = Subject.objects.filter(
                name=form.cleaned_data["name"],
            ).exists()

            if existing_subject:
                messages.error(request, "Erro - Matéria já foi cadastrada!")
                return redirect(f"{request.path}")

            form.instance.course = course
            form.instance.year = datetime.datetime.now().year
            form.save()
            return redirect(f"/subjects/{course.id}")
        return self.render_to_response(self.get_context_data(form=form))


class EditSubjectPageView(TemplateView):
    template_name = "pages/subjects/edit-subject.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject_id = self.kwargs.get("subject_id")
        subject = get_object_or_404(Subject, id=subject_id)

        # Filter Selectors
        context["courses"] = Course.objects.all()

        # Protected delete error
        request = self.request
        if request.GET.get("error") == "protected":
            messages.error(
                request,
                "Erro - Você não pode remover matérias com ofertas associadas!",
            )

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
                "icon": "images/icons/icon-edit-green.svg",
                "name": "Editar Matéria",
            },
        ]

        context["subject"] = subject
        context["course_types"] = [course[0] for course in COURSE_TYPE]

        return context

    def post(self, request, *args, **kwargs):
        subject_id = self.kwargs.get("subject_id")
        subject = get_object_or_404(Subject, id=subject_id)
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect("courses")
        return self.render_to_response(self.get_context_data(form=form))


class OffersPageView(TemplateView):
    template_name = "pages/offers/offers.html"
    paginate_by = 10

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
                "name": "Ofertas",
                "url": "offers",
            },
        ]

        # Filter Selectors
        context["selector_teachers"] = Teacher.objects.all()
        context["selector_subjects"] = Subject.objects.all()

        # Table
        filters = {}
        if "teacher" in self.request.GET:
            filters["teacher__id"] = self.request.GET["teacher"]
        if "subject" in self.request.GET:
            filters["subject__id"] = self.request.GET["subject"]

        offers = Offer.objects.filter(**filters)

        if "search" in self.request.GET:
            offers = offers.filter(
                Q(subject__name__icontains=self.request.GET["search"]),
            )

        paginator = Paginator(offers, self.paginate_by)
        page_number = self.request.GET.get("page")

        try:
            all_offers = paginator.page(page_number)
        except PageNotAnInteger:
            all_offers = paginator.page(1)
        except EmptyPage:
            all_offers = paginator.page(paginator.num_pages)

        context["offers"] = all_offers

        return context


class DeleteOfferView(View):
    def get(self, request, offer_id):
        offer = get_object_or_404(Offer, id=offer_id)
        try:
            offer.delete()
            return redirect("offers")
        except ProtectedError:
            messages.error(
                request,
                "Erro - Você não pode remover ofertas com alunos associados!",
            )
            return redirect("offers")


class CreateOfferPageView(TemplateView):
    template_name = "pages/offers/create-offer.html"

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
                "url": "offers",
            },
            {
                "icon": "images/icons/icon-edit-green.svg",
                "name": "Criar Oferta",
            },
        ]

        context["selector_teachers"] = Teacher.objects.all()
        context["selector_subjects"] = Subject.objects.all()

        return context

    def post(self, request, *args, **kwargs):
        form = OfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("offers")
        else:
            print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))


class EditOfferPageView(TemplateView):
    template_name = "pages/offers/edit-offer.html"

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
                "url": "offers",
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
            return redirect("offers")
        return self.render_to_response(self.get_context_data(form=form))


class OfferDetailsPageView(TemplateView):
    template_name = "pages/offers/offer-details.html"
    paginate_by = 10

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
                "url": "offers",
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
        
        context["selector_students"] = Student.objects.filter(course__in=offer.subject.courses.all()).exclude(id__in=offer.enrollments.values_list('student_id', flat=True))

        return context

class AddStudentToOfferView(View):
    def post(self, request, offer_id):
        offer = get_object_or_404(Offer, id=offer_id)
        student_id = request.POST.get('student')
        student = get_object_or_404(Student, id=student_id)
        
        if not Enrollment.objects.filter(offer=offer, student=student).exists():
            Enrollment.objects.create(offer=offer, student=student, YearSemesterReference=student.reference_period)
        
        return redirect(f'/offers/details/{offer.id}')
