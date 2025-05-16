from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from sistema_pei.core import constants

from .models import Campus
from .models import Student
from .models import StudentFile
from .models import Teacher

User = get_user_model()


class PeopleInviteForm(forms.Form):
    email = forms.EmailField(
        max_length=constants.MAX_CHAR_FIELD_NAME_LENGTH,
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Tipo de Usuário",
        required=True,
    )
    sector = forms.ChoiceField(
        choices=User.Sector.choices,
        label="Setor",
        required=True,
    )


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


class TeacherForm(forms.ModelForm):
    campus = forms.ModelChoiceField(
        queryset=Campus.objects.all(),
        label="Campus",
        required=True,
        empty_label=_("Selecione um campus..."),
        widget=forms.Select(
            attrs={
                "class": "outline-none text-[18px] rounded-lg h-[48px] border px-[10px] border-slate-300 w-full text-slate-500 appearance-none bg-neutral-50",  # noqa: E501
            },
        ),
    )

    class Meta:
        model = Teacher
        fields = (
            "name",
            "email",
            "campus",
            "photoAlt",
            "code",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "outline-none placeholder:text-[18px] placeholder:text-slate-500 rounded-lg bg-neutral-50 w-full h-[48px] px-[10px] border border-slate-300 mt-[16px]",  # noqa: E501
                    "placeholder": "Digite o nome do docente...",
                },
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "outline-none placeholder:text-[18px] placeholder:text-slate-500 rounded-lg bg-neutral-50 w-full h-[48px] px-[10px] border border-slate-300 mt-[16px]",  # noqa: E501
                    "placeholder": "Digite o email do docente...",
                },
            ),
            "photoAlt": forms.FileInput(
                attrs={
                    "class": "font-sans text-slate-900 block file:cursor-pointer text-sm file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-green-200 file:text-green-700 hover:file:bg-green-300",  # noqa: E501
                    "id": "photoAlt",
                    "accept": "image/png, image/jpeg",
                    "onchange": "previewImage(event)",
                },
            ),
            "code": forms.TextInput(
                attrs={
                    "class": "outline-none placeholder:text-[18px] placeholder:text-slate-500 rounded-lg bg-neutral-50 w-full h-[48px] px-[10px] border border-slate-300 mt-[16px]",  # noqa: E501
                    "placeholder": "Digite a matrícula...",
                },
            ),
        }


class AdminStudentForm(forms.ModelForm):
    """
    Formulário usado no admin do Django.
    Ele garante que a validação de "período atual" ocorra.
    """

    class Meta:
        model = Student
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminStudentForm, self).__init__(*args, **kwargs)
        self.fields["course"].empty_label = "Selecione um curso..."

    def clean_reference_period(self):
        reference_period = self.cleaned_data.get("reference_period")
        course = self.cleaned_data.get("course")

        if course and reference_period:
            number_of_periods = course.number_of_periods
            if reference_period > number_of_periods:
                msg = (
                    f"O período de referência não pode ser maior que o número "
                    f"máximo de períodos ({number_of_periods}) do curso selecionado."
                )
                raise ValidationError(
                    msg,
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
        exclude = ("created_by", "updated_by")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "user" in self.fields:
            self.fields["user"].required = False

    def clean_files(self):
        files = self.cleaned_data.get("files", [])
        allowed_extensions = [
            ".pdf",
            ".doc",
            ".docx",
            ".jpg",
            ".jpeg",
            ".png",
            ".xlsx",
            ".xls",
        ]

        for file in files:
            if not any(file.name.lower().endswith(ext) for ext in allowed_extensions):
                msg = (
                    f"Arquivo {file.name} possuia uma extensão não suportada. "
                    f"As extensões suportadas são: {', '.join(allowed_extensions)}"
                )
                raise ValidationError(
                    msg,
                )

        return files


class ViewEditDataStudentForm(AdminStudentForm):
    class Meta(AdminStudentForm.Meta):
        exclude = (
            "created_by",
            "updated_by",
            "personal_history",
            "creation_reasons",
            "abilities",
            "dificulties",
            "general_necessitie",
            "specific_necessities",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["educational_necessities"].required = False
        self.fields["course"].required = False
        self.fields["sectors"].required = False
        if "user" in self.fields:
            self.fields["user"].required = False


class ViewEdithistoricStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = (
            "created_by",
            "updated_by",
            "name",
            "email",
            "image",
            "registration",
            "educational_necessities",
            "course",
            "reference_period",
            "sectors",
        )


class StudentFilesForm(forms.ModelForm):
    files = MultipleFileField(required=False)

    class Meta:
        model = StudentFile
        fields = ["files"]

    def __init__(self, *args, **kwargs):
        super(StudentFilesForm, self).__init__(*args, **kwargs)
        self.fields["files"].required = False

    def clean_files(self):
        files = self.cleaned_data.get("files", [])
        allowed_extensions = [
            ".pdf",
            ".doc",
            ".docx",
            ".jpg",
            ".jpeg",
            ".png",
            ".xlsx",
            ".xls",
        ]

        for file in files:
            if not any(file.name.lower().endswith(ext) for ext in allowed_extensions):
                msg = (
                    f"Arquivo {file.name} possui uma extensão não suportada. "
                    f"As extensões suportadas são: {', '.join(allowed_extensions)}"
                )
                raise ValidationError(
                    msg,
                )

        return files
