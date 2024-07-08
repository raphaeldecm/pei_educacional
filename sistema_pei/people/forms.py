from django import forms
from .models import Student, StudentFile
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class AdminStudentForm(forms.ModelForm):
    """
    Formulário usado no admin do Django. Ele garante que a validação de "período atual" ocorra.
    """
    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AdminStudentForm, self).__init__(*args, **kwargs)
        self.fields['responsible_person'].empty_label = "Selecione um responsável..."
        self.fields['course'].empty_label = "Selecione um curso..."


    def clean_reference_period(self):
        reference_period = self.cleaned_data.get('reference_period')
        course = self.cleaned_data.get('course')

        if course and reference_period:
            number_of_periods = course.number_of_periods
            if reference_period > number_of_periods:
                raise ValidationError(
                    f"O período de referência não pode ser maior que o número máximo de períodos ({number_of_periods}) do curso selecionado."
                )

        return reference_period

class ViewStudentForm(AdminStudentForm):
    """
    Formulário para ser usado no Template de cadastro do aluno.
    Os campos 'created_by', 'updated_by' devem ser atualizados na view.
    Files: Anexos do estudante.
    """

    files = MultipleFileField(required=False)

    class Meta(AdminStudentForm.Meta):
        exclude = ('created_by', 'updated_by')
