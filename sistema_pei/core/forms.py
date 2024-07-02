from sistema_pei.academics.models import Courses, Subject
from django import forms

class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['name', 'period', 'course_type']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'teacher', 'subject_type']