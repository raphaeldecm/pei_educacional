import re

from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.generic.edit import CreateView
from django_filters.views import FilterView
from django.contrib.auth import get_user_model

from sistema_pei.core import constants
from sistema_pei.core.mixins import TitleViewMixin
from sistema_pei.people.filters import TeacherFilter
from sistema_pei.people.models import Student
from sistema_pei.people.models import StudentFile
from sistema_pei.people.models import Teacher
from sistema_pei.people.models import User
from sistema_pei.users.models import Sector

from .forms import TeacherForm
from .forms import ViewStudentForm
from .forms import UserInviteForm

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


class UsersPageView(generic.View):
    template_name = "people/invite_people.html"

    def get(self, request):
        form = UserInviteForm()
        return render(request, self.template_name, {"form": form})

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
