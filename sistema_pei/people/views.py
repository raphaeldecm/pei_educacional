from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import generic
from django.views.generic.edit import CreateView
from django_filters.views import FilterView

from sistema_pei.core import constants
from sistema_pei.people.filters import TeacherFilter
from sistema_pei.people.models import Student
from sistema_pei.people.models import StudentFile
from sistema_pei.people.models import Teacher
from sistema_pei.people.models import User

from .forms import ViewStudentForm


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
    else:
        return render(request, "403.html")

class TeacherListView(FilterView, generic.ListView):
    model = Teacher
    paginate_by = constants.DEFAULT_PAGE_SIZE
    filterset_class = TeacherFilter
    template_name = "people/teacher_list.html"

class TeacherCreateView(CreateView):
    model = Teacher
    fields = ["name", "email", "campus"]
    template_name = "people/teacher_create.html"
    success_url = reverse_lazy("people:teacher_create")

    def form_valid(self, form):
        response = super().form_valid(form)

        name_value = form.cleaned_data["name"]
        success_message = f"Professor {name_value} cadastrado com sucesso"
        messages.success(self.request, success_message)

        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)

        error_message = "Erro ao cadastrar professor!"
        messages.error(self.request, error_message)

        return response

class TeacherEditView(generic.UpdateView):
    model = Teacher
    fields = ["name", "email", "campus"]
    template_name = "people/teacher_edit.html"
    success_url = reverse_lazy("people:teacher_list")

    def form_valid(self, form):
        response = super().form_valid(form)

        name_value = form.cleaned_data["name"]
        success_message = f"Professor {name_value} alterado com sucesso"
        messages.success(self.request, success_message)

        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)

        error_message = "Erro ao alterar professor!"
        messages.error(self.request, error_message)

        return response

class TeacherDeleteView(generic.DeleteView):
    model = Teacher
    template_name = "people/teacher_delete.html"
    success_url = reverse_lazy("people:teacher_list")

    def delete(self, request, *args, **kwargs):
        teacher = self.get_object()
        teacher.delete()

        name_value = teacher.name
        success_message = f"Professor {name_value} deletado com sucesso"
        messages.success(self.request, success_message)

        return redirect(self.success_url)

class TeacherDetailView(generic.DetailView):
    model = Teacher
    template_name = "people/teacher_detail.html"
    context_object_name = "teacher"


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
