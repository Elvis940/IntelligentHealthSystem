from django import forms
from .models import UserSymptom, Disease

class UserSymptomForm(forms.ModelForm):
    class Meta:
        model = UserSymptom
        fields = ['patient_id', 'symptoms']
        widgets = {
            'patient_id': forms.TextInput(attrs={'class': 'form-control'}),
            'symptoms': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = ['name', 'symptoms', 'test_results', 'recommendation', 'medicine']
