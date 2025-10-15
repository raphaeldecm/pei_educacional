from django import forms
from django.db.models.functions import Lower

from sistema_pei.academics import models


class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ["name", "period", "course_type", "duration_type", "number_of_periods"]


class OfferForm(forms.ModelForm):
    class Meta:
        model = models.Offer
        fields = ["status", "subject", "year", "teachers", "course", "semester"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["teachers"].queryset = models.Teacher.objects.order_by("name")


class SubjectForm(forms.ModelForm):
    matrix = forms.ModelChoiceField(
        queryset=models.Matrix.objects.all(),
        label="matix",
        required=False,
    )

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
            "assessments",
            "matrix",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["courses"].queryset = models.Course.objects.all().order_by(
            Lower("name"),
        )


class CSVImportForm(forms.Form):
    file = forms.FileField(label="Arquivo CSV")


class MatrixForm(forms.ModelForm):
    class Meta:
        model = models.Matrix
        fields = ["code", "description", "year", "active"]
