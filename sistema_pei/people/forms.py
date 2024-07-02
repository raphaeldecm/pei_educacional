from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'serie', 'responsible_person', 'registration',
                  'personal_history', 'image', 'general_necessitie', 'creation_reasons',
                  'educational_necessities', 'abilities', 'dificulties', 'specific_necessities']

