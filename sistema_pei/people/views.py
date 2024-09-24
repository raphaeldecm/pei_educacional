from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.generic.edit import CreateView
from django_filters.views import FilterView

from sistema_pei.core import constants
from sistema_pei.core.mixins import TitleViewMixin
from sistema_pei.people.filters import TeacherFilter
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
    template_name = "people/teacher_list.html"
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


class StudentCreateView(CreateView):
    model = Student
    form_class = ViewStudentForm
    template_name = "pages/student_create.html"
    success_url = reverse_lazy("student_create")

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
