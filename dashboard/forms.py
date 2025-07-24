from django import forms
from patients.models import Patient
from symptom_checker.models import VitalSign

class VitalSignForm(forms.ModelForm):
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), required=True, label="Patient")

    class Meta:
        model = VitalSign
        fields = ['patient', 'disease', 'temperature', 'heart_rate', 'respiratory_rate', 'blood_pressure', 'notes']