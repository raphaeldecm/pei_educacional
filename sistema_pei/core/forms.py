from django import forms

from sistema_pei.academics.models import Course, Offer
from sistema_pei.academics.models import Enrollment
from sistema_pei.academics.models import Subject


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "period", "course_type", "durationType", "number_of_periods"]


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "subject_type", "courses"]


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ["grade1", "grade2", "grade3", "grade4"]
        
class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ["status", "subject", "year", "teacher"]
