from itertools import count
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.core.paginator import Paginator, PageNotAnInteger
from django.template.loader import render_to_string
from django.db.models import Q, Count
from django.contrib.sites.shortcuts import get_current_site
from allauth.account.models import EmailAddress
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db import IntegrityError
from django.views.generic import View
import datetime
import re

from django.conf import settings
from sistema_pei.academics.constants import COURSE_TYPE
from sistema_pei.academics.models import Courses, StudentGradesAnual, StudentGradesSemestral, Subject
from sistema_pei.core.forms import CourseForm, SubjectForm
from sistema_pei.educational_plan.models import Pei
from sistema_pei.people.models import Student, StudentFile, Teacher, User
from django.contrib.auth.models import Group

from sistema_pei.users.models import Sector


class HomePageView(TemplateView):
    template_name = "pages/home.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filter Selectors
        context['selector_courses'] = Courses.objects.all()
        context['selector_teachers'] = Teacher.objects.all()
        context['selector_Subjects'] = Subject.objects.all()

        # Cards
        context['pending_peis'] = Pei.objects.filter(
            status='NOT_START').count()
        context['in_progress_peis'] = Pei.objects.filter(
            status='IN_PROGRESS').count()
        context['filled_peis'] = Pei.objects.filter(status='FEEDBACK').count()
        context['finished_peis'] = Pei.objects.filter(
            status='COMPLETED').count()

        # Table
        filters = {}
        if 'course' in self.request.GET:
            filters['subject__course__id'] = self.request.GET['course']
        if 'teacher' in self.request.GET:
            filters['subject__teacher__id'] = self.request.GET['teacher']
        if 'period' in self.request.GET:
            filters['subject__course__period'] = self.request.GET['period']
        if 'status' in self.request.GET:
            filters['status'] = self.request.GET['status']
        if 'subject' in self.request.GET:
            filters['subject__id'] = self.request.GET['subject']

        peis_list = Pei.objects.filter(**filters)

        if 'search' in self.request.GET:
            peis_list = peis_list.filter(Q(student__name__icontains=self.request.GET['search']) | Q(student__registration__icontains=self.request.GET['search']))

        peis_list = peis_list.order_by('id')
        paginator = Paginator(peis_list, self.paginate_by)
        page_number = self.request.GET.get('page')

        try:
            all_peis = paginator.page(page_number)
        except PageNotAnInteger:
            all_peis = paginator.page(1)

        context['all_peis'] = all_peis

        return context

class UsersPageView(TemplateView):
    template_name = "pages/users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        context['sectors'] = Sector.objects.all()

        request = self.request
        if request.GET.get('alert') == "success":
            context['messages'] = ["Convite enviado!"]
        elif request.GET.get('alert') == "error":
            context['messages'] = ["Usuário já cadastrado!"]

        return context

    def post(self, request, *args, **kwargs):
        recipient = request.POST.get('recipient')
        username = re.split(r'@', recipient)[0]

        sector = Sector.objects.get(id=request.POST.get('sector'))
        group = Group.objects.get(id=request.POST.get('group'))
        current_site = get_current_site(request)

        try:
            user = User.objects.create_user(email=recipient, name=username, is_active=False, sector=sector)
            group.user_set.add(user)
            EmailAddress.objects.create(user=user, email=recipient, verified=True, primary=True)
        except IntegrityError:
            return HttpResponseRedirect('?alert=error')

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = f"http://{current_site.domain}/activate/{uid}/{token}/"

        context = {
            'sector_name': sector.name,
            'group_name': group.name,
            'user': username,
            'activation_link': activation_link,
        }

        html_message = render_to_string('layouts/email_template.html', context)

        email = EmailMessage(
            subject="PEIs - Convite",
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient]
        )

        email.content_subtype = "html"

        try:
            email.send()
            return HttpResponseRedirect('?alert=success')
        except Exception as e:
            return HttpResponse(f"Erro ao enviar o e-mail: {e}")

class ProfilePageView(TemplateView):
    template_name = "pages/profile.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        
        # Profile data
        context['student'] = student
        context['student_files'] = StudentFile.objects.filter(student=student)

        # Tabs
        context['active_tab'] = self.request.GET.get('tab', 'general')
        
        ## Tab General
        student_peis = context['student_peis'] = Pei.objects.filter(student=student)

        ### Filters Selectors
        context['selector_teachers'] = Teacher.objects.all()

        ### Filters
        filters = {}
        if 'course' in self.request.GET:
            filters['subject__course__id'] = self.request.GET['course']
        if 'teacher' in self.request.GET:
            filters['subject__teacher__id'] = self.request.GET['teacher']
        if 'period' in self.request.GET:
            filters['subject__course__period'] = self.request.GET['period']
        if 'status' in self.request.GET:
            filters['status'] = self.request.GET['status']

        student_peis = student_peis.filter(**filters)

        if 'search' in self.request.GET:
            student_peis = student_peis.filter(Q(subject__name__icontains=self.request.GET['search']))
        
        student_peis = student_peis.order_by('id')
        paginator = Paginator(student_peis, self.paginate_by)
        page_number = self.request.GET.get('page')

        try:
            student_peis = paginator.page(page_number)
        except PageNotAnInteger:
            student_peis = paginator.page(1)

        context['student_peis'] = student_peis
        ## Tab Notes
        
        if 'selectedPeriod' in self.request.GET:
            pass
        
        # Pegar notas de acordo com tipo de duração do curso
        if (student.course.durationType == "SEMESTER"):
            context["student_notes"] = StudentGradesSemestral.objects.filter(student=student)
        else:
            context["student_notes"] = StudentGradesAnual.objects.filter(student=student)
        
        
        
            
        ## Tab Edit
        
        
        # Breadcrumbs
        context['breadcrumbs_data'] = [
            {
                "icon":"images/icons/icon-home-green.svg",
                "name":"Home",
                "url":"home"
            },
            {
                "icon":"images/icons/icon-courses-green.svg",
                "name":student.name,
            }
        ]
        return context


class CoursesPageView(TemplateView):
    template_name = "pages/courses/courses.html"
    paginate_by=10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Breadcrumbs
        context['breadcrumbs_data'] = [
            {
                "icon":"images/icons/icon-home-green.svg",
                "name":"Home",
                "url":"home"
            },
            {
                "icon":"images/icons/icon-courses-green.svg",
                "name":"Cursos",
            }
        ]

        # Filter Selectors
        context['course_types']=[course[0] for course in COURSE_TYPE]

        # Table
        filters = {}
        if 'period' in self.request.GET:
            filters['period'] = self.request.GET['period']
        if 'type' in self.request.GET:
            filters['course_type'] = self.request.GET['type']

        courses_list = Courses.objects.filter(**filters)

        if 'search' in self.request.GET:
            courses_list = courses_list.filter(Q(name__icontains=self.request.GET['search']))


        courses_list = courses_list.annotate(num_subjects=Count('subjects')).order_by('id')
        paginator = Paginator(courses_list, self.paginate_by)
        page_number = self.request.GET.get('page')

        try:
            all_courses = paginator.page(page_number)
        except PageNotAnInteger:
            all_courses = paginator.page(1)
        except EmptyPage:
            all_courses = paginator.page(paginator.num_pages)

        context['courses'] = all_courses

        return context

class CreateCoursesPageView(TemplateView):
    template_name = "pages/courses/create-course.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Breadcrumbs
        context['breadcrumbs_data'] = [
            {
                "icon":"images/icons/icon-home-green.svg",
                "name":"Home",
                "url":"home"
            },
            {
                "icon":"images/icons/icon-courses-green.svg",
                "name":"Cursos",
                "url":"courses"
            },
            {
                "icon":"images/icons/icon-edit-green.svg",
                "name":"Criar Curso",
            }
        ]

        context['course_types']=[course[0] for course in COURSE_TYPE]
        return context

    def post(self, request, *args, **kwargs):
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses')
        return self.render_to_response(self.get_context_data(form=form))

class DeleteCourseView(View):
    def get(self, request, course_id):
        course = get_object_or_404(Courses, id=course_id)
        course.delete()
        return redirect('courses')


class EditCoursePageView(TemplateView):
    template_name = "pages/courses/edit-course.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Courses, id=course_id)
        course_subjects = course.subjects.all()

        # Breadcrumbs
        context['breadcrumbs_data'] = [
            {
                "icon":"images/icons/icon-home-green.svg",
                "name":"Home",
                "url":"home"
            },
            {
                "icon":"images/icons/icon-courses-green.svg",
                "name":"Cursos",
                "url":"courses"
            },
            {
                "icon":"images/icons/icon-edit-green.svg",
                "name":"Editar Curso",
            }
        ]

        filters = {}
        if 'search_subject' in self.request.GET:
            filters['search_subject'] = self.request.GET['search_subject']
            course_subjects = course_subjects.filter(Q(name__icontains=self.request.GET['search_subject']))

        context['course'] = course
        context['course_subjects'] = course_subjects
        context['course_types']=[course[0] for course in COURSE_TYPE]

        return context

    def post(self, request, *args, **kwargs):
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Courses, id=course_id)
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses')
        return self.render_to_response(self.get_context_data(form=form))


class DeleteSubjectView(View):
    def get(self, request, subject_id):
        subject = get_object_or_404(Subject, id=subject_id)
        subject.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class SubjectsPageView(TemplateView):
    template_name = "pages/subjects/subjects.html"
    paginate_by=10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Courses, id=course_id)
        course_subjects = course.subjects.all()
        context['course'] = course

        # Breadcrumbs
        context['breadcrumbs_data'] = [
            {
                "icon":"images/icons/icon-home-green.svg",
                "name":"Home",
                "url":"home"
            },
            {
                "icon":"images/icons/icon-courses-green.svg",
                "name":"Cursos",
                "url":"courses"
            },
            {
                "icon":"images/icons/icon-courses-green.svg",
                "name":"Matérias"
            },
        ]

        # Filter Selectors
        context['teachers'] = Teacher.objects.all()

        # Table
        filters = {}
        if 'duration' in self.request.GET:
            filters['subject_type'] = self.request.GET['duration']
        if 'teacher' in self.request.GET:
            filters['teacher'] = self.request.GET['teacher']

        course_subjects = course_subjects.filter(**filters)

        if 'search' in self.request.GET:
            course_subjects = course_subjects.filter(Q(name__icontains=self.request.GET['search']))


        paginator = Paginator(course_subjects, self.paginate_by)
        page_number = self.request.GET.get('page')

        try:
            all_course_subjects = paginator.page(page_number)
        except PageNotAnInteger:
            all_course_subjects = paginator.page(1)
        except EmptyPage:
            all_course_subjects = paginator.page(paginator.num_pages)

        context['course_subjects'] = all_course_subjects


        return context

class CreateSubjectPageView(TemplateView):
    template_name = "pages/subjects/create-subject.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Courses, id=course_id)
        context['course'] = course

        # Breadcrumbs
        context['breadcrumbs_data'] = [
            {
                "icon":"images/icons/icon-home-green.svg",
                "name":"Home",
                "url":"home"
            },
            {
                "icon":"images/icons/icon-courses-green.svg",
                "name":"Cursos",
                "url":"courses"
            },
            {
                "icon":"images/icons/icon-edit-green.svg",
                "name":"Criar Matéria"
            },
        ]
        context['course_types']=[course[0] for course in COURSE_TYPE]
        context['teachers']= Teacher.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = SubjectForm(request.POST)
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Courses, id=course_id)

        if form.is_valid():
            form.instance.course = course
            form.instance.year = datetime.datetime.now().year
            form.save()
            return redirect(f'/subjects/{course.id}')
        return self.render_to_response(self.get_context_data(form=form))

class EditSubjectPageView(TemplateView):
    template_name = "pages/subjects/edit-subject.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject_id = self.kwargs.get('subject_id')
        subject = get_object_or_404(Subject, id=subject_id)

        # Breadcrumbs
        context['breadcrumbs_data'] = [
            {
                "icon":"images/icons/icon-home-green.svg",
                "name":"Home",
                "url":"home"
            },
            {
                "icon":"images/icons/icon-courses-green.svg",
                "name":"Cursos",
                "url":"courses"
            },
            {
                "icon":"images/icons/icon-edit-green.svg",
                "name":"Editar Matéria"
            },
        ]

        subject_students = subject.students.all()

        if 'search_student' in self.request.GET:
            search_query = self.request.GET['search_student']
            subject_students = subject.students.filter(Q(name__icontains=search_query))


        students_with_courses = []
        for student in subject_students:
            course_name = subject.course.name if subject.course else "Curso não definido"
            students_with_courses.append({
                'student': student,
                'course_name': course_name
            })

        context['subject'] = subject
        context['subject_students_with_courses'] = students_with_courses
        context['teachers']= Teacher.objects.all()
        context['course_types']=[course[0] for course in COURSE_TYPE]

        return context

    def post(self, request, *args, **kwargs):
        subject_id = self.kwargs.get('subject_id')
        subject = get_object_or_404(Subject, id=subject_id)
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('courses')
        return self.render_to_response(self.get_context_data(form=form))
