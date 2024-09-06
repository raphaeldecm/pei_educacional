from django import forms

from sistema_pei.academics.models import Offer


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ["status", "subject", "year", "teacher", "course"]
        
        widgets = {
            "subject": forms.Select(attrs={
                "class": "outline-none text-[18px] rounded-lg h-[48px] border px-[10px] border-slate-300 [&_option:bg-red-100] w-full text-slate-300 appearance-none bg-neutral-50"
            }),
            "course": forms.Select(attrs={
               "class": "outline-none text-[18px] rounded-lg h-[48px] border px-[10px] border-slate-300 [&_option:bg-red-100] w-full text-slate-300 appearance-none bg-neutral-50" 
            }),
            "teacher": forms.Select(attrs={
                "class": "outline-none text-[18px] rounded-lg h-[48px] border px-[10px] border-slate-300 [&_option:bg-red-100] w-full text-slate-300 appearance-none bg-neutral-50",
            }),
            "year": forms.NumberInput(attrs={
               "class": "outline-none placeholder:text-[18px] placeholder:text-slate-300 rounded-lg bg-neutral-50 w-full h-[48px] px-[10px] border border-slate-300 mt-[16px]",
               "placeholder": "Digite o ano..." 
            }),
            "status": forms.Select(attrs={
                "class": "outline-none text-[18px] rounded-lg h-[48px] border px-[10px] border-slate-300 [&_option:bg-red-100] w-full text-slate-300 appearance-none bg-neutral-50",
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].empty_label = "Selecione a disciplina..."
        self.fields['teacher'].empty_label = "Selecione o professor..."
        self.fields['course'].empty_label = "Selecione o curso..."
        self.fields['status'].empty_label = "Selecione o status..."
