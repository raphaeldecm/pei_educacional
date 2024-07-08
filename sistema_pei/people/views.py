from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect
from sistema_pei.people.models import User, Student, StudentFile
from django.views.generic.edit import CreateView
from django.contrib import messages

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

        user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
        login(request, user)

        return redirect('/')
    else:
        return render(request, '403.html')


class StudentCreateView(CreateView):
    model = Student
    form_class = ViewStudentForm
    template_name = 'pages/student_create.html'
    success_url = reverse_lazy('student_create')

    def form_valid(self, form):
        student = form.save(commit=False)
        student.created_by = self.request.user
        student.updated_by = None
        student.save()

        files = form.cleaned_data.get('files')
        if files:
            for file in files:
                StudentFile.objects.create(student=student, file=file)

        response = super().form_valid(form)

        name_value = form.cleaned_data['name']
        success_message = f'estudante {name_value} cadastrado com sucesso'
        messages.success(self.request, success_message)

        return response


    def form_invalid(self, form):
        response = super().form_invalid(form)

        error_message = f'Erro ao cadastrar usuario!'
        messages.error(self.request, error_message)

        return response
