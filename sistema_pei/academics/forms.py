from django import forms

from sistema_pei.academics import models
from sistema_pei.educational_plan.models import Pei


class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ["name", "period", "course_type", "duration_type", "number_of_periods"]


class OfferForm(forms.ModelForm):
    class Meta:
        model = models.Offer
        fields = ["status", "subject", "year", "teacher", "course", "semester"]


class SubjectForm(forms.ModelForm):
    class Meta:
        model = models.Subject
        fields = [
            "name",
            "subject_type",
            "courses",
            "objective",
            "content",
            "methodology",
            "resources",
            "assessments"
        ]
