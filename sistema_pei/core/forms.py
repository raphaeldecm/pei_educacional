from django import forms

from sistema_pei.academics.models import Enrollment
from sistema_pei.academics.models import Subject


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "subject_type", "courses"]


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = [
            "grade1", "grade2", "grade3", "grade4",
            "absences1", "absences2", "absences3", "absences4"
        ]

