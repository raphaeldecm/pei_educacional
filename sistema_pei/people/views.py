from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views import View, generic
from django.views.generic.edit import CreateView
from django_filters.views import FilterView
from sistema_pei.people.forms import StudentFilesForm, ViewEditDataStudentForm, ViewEdithistoricStudentForm
from django.db.models import Q
from django.views.generic import TemplateView
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator

from sistema_pei.academics.models import Enrollment
from sistema_pei.core import constants
from sistema_pei.core.forms import EnrollmentForm
from sistema_pei.core.mixins import ProtectedErrorMessageMixin, TitleViewMixin
from sistema_pei.educational_plan.models import Pei
from sistema_pei.people.filters import StudentFilter, TeacherFilter
from sistema_pei.people.models import Student
from sistema_pei.people.models import StudentFile
from sistema_pei.people.models import Teacher
from sistema_pei.people.models import User

from .forms import TeacherForm
from .forms import ViewStudentForm

User = get_user_model()


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        user.backend = "allauth.account.auth_backends.AuthenticationBackend"
        login(request, user)

        return redirect("/")
    return render(request, "403.html")


class TeacherListView(LoginRequiredMixin, TitleViewMixin, FilterView, generic.ListView):
    model = Teacher
    title = _("Docentes")
    paginate_by = constants.DEFAULT_PAGE_SIZE
    filterset_class = TeacherFilter
    template_name = "people/teacher/teacher_list.html"
    ordering = ["name"]


class TeacherCreateView(
    LoginRequiredMixin,
    TitleViewMixin,
    SuccessMessageMixin,
    generic.CreateView,
):
    model = Teacher
    title = _("Cadastrar Docente")
    form_class = TeacherForm
    success_url = reverse_lazy("people:teacher_list")
    success_message = _("O professor foi cadastrado com sucesso.")
    template_name = "people/teacher/teacher_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class TeacherUpdateView(
    LoginRequiredMixin,
    TitleViewMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    model = Teacher
    title = _("Atualizar Docente")
    form_class = TeacherForm
    success_url = reverse_lazy("people:teacher_list")
    success_message = _("O professor foi atualizado com sucesso.")
    template_name = "people/teacher/teacher_form.html"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class TeacherDeleteView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Teacher
    success_url = reverse_lazy("people:teacher_list")
    success_message = _("O professor foi excluído com sucesso.")


class TeacherDetailView(LoginRequiredMixin, TitleViewMixin, generic.DetailView):
    model = Teacher
    context_object_name = "teacher"
    title = _("Detalhes do Docente")
    template_name = "people/teacher/teacher_detail.html"

class StudentListView(
    LoginRequiredMixin,
    TitleViewMixin,
    FilterView,
    generic.ListView,
):
    model = Student
    title = _("Alunos")
    paginate_by = constants.DEFAULT_PAGE_SIZE
    filterset_class = StudentFilter
    template_name = "people/student/student_list.html"

class StudentDeleteView(ProtectedErrorMessageMixin, LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Student
    success_url = reverse_lazy("people:student_list")
    success_message = _("O aluno foi excluído com sucesso.")
    protected_warning_message = _(
        "Não é possível excluir o aluno, pois ele possui ofertas associadas.",
    )

class StudentCreateView(CreateView):
    model = Student
    form_class = ViewStudentForm
    template_name = "people/student/student_create.html"
    success_url = reverse_lazy("people:student_create")

    def form_valid(self, form):
        student = form.save(commit=False)
        student.created_by = self.request.user
        student.updated_by = None
        student.save()

        files = form.cleaned_data.get("files")
        if files:
            for file in files:
                StudentFile.objects.create(student=student, file=file)

        response = super().form_valid(form)

        name_value = form.cleaned_data["name"]
        success_message = f"estudante {name_value} cadastrado com sucesso"
        messages.success(self.request, success_message)

        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)

        error_message = "Erro ao cadastrar usuario!"
        messages.error(self.request, error_message)

        return response


class ProfilePageView(TemplateView):
    template_name = "people/student/profile.html"
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
                f"/people/profile/{enrollment.student.id}?tab=edit_student_data&sub_tab=edit_notes&selectedPeriod={selected_period}",
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
            f"/people/profile/{student.id}?tab=edit_student_data&sub_tab=edit_personal_data#tab",
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
            f"/people/profile/{student.id}?tab=edit_student_data&sub_tab=edit_historic#tab",
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
            f"/people/profile/{student.id}?tab=edit_student_data&sub_tab=edit_files#tab",
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
            f"/people/profile/{student.id}?tab=edit_student_data&sub_tab=edit_files#tab",
        )

