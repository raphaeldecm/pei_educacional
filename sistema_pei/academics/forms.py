from django import forms

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
        ]


class CSVImportForm(forms.Form):
    file = forms.FileField(label="Arquivo CSV")
