from django import forms

from sistema_pei.academics.models import Offer


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ["status", "subject", "year", "teacher", "course"]