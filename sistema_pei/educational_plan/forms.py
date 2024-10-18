from django import forms
from django.utils.translation import gettext_lazy as _

from sistema_pei.educational_plan.models import Answer, Comment, Pei


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
            "academic_opinion_1",
            "academic_opinion_2",
            "academic_opinion_3",
            "academic_opinion_4",
            "academic_opinion_final",
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "text",
        ]

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [
            "text",
        ]
