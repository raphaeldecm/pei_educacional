from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ('created_by', 'updated_by')

    def __init__(self, *args, **kwargs):
            super(StudentForm, self).__init__(*args, **kwargs)
            self.fields['responsible_person'].empty_label = "Selecione um responsável..."
            self.fields['course'].empty_label = "Selecione um curso..."

