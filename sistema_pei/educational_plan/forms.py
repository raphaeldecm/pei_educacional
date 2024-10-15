from django import forms
from django.utils.translation import gettext_lazy as _

from sistema_pei.educational_plan.models import Comment, Pei


class PeiForm(forms.ModelForm):
    class Meta:
        model = Pei
        fields = [
            "enrollment",
            "status",
            "objective",
            "adapted_objective",
            "content",
            "adapted_content",
            "methodology",
            "adapted_methodology",
            "resources",
            "adapted_resources",
            "assessments",
            "adapted_assessments",
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "text",
        ]
