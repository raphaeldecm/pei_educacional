from sistema_pei.academics.models import Courses
from django import forms

class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['name', 'period', 'course_type']