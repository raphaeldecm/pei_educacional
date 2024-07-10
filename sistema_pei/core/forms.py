from sistema_pei.academics.models import Courses, Subject
from django import forms

class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['name', 'period', 'course_type', 'number_of_periods']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'teacher', 'subject_type']
        
