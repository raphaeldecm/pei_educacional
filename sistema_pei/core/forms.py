from django import forms

from sistema_pei.academics.models import Course
from sistema_pei.academics.models import Subject


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "period", "course_type", "durationType", "number_of_periods"]


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "subject_type", "courses"]
