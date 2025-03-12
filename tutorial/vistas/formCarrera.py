from django import forms
from ..models import Carrera

class FormCarrera(forms.ModelForm):
    class Meta:
        model = Carrera
        fields = ["name", "description"]
        #fields = '__all__'