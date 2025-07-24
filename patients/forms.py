from django import forms

class PatientRegistrationForm(forms.Form):
    patient_id = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=100, required=True)
    age = forms.IntegerField(min_value=0, required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=True)
    status = forms.ChoiceField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Pending', 'Pending')], required=True)
