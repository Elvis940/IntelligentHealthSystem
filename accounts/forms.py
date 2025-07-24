from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account




class UserRegistrationForm(UserCreationForm):
    image = forms.ImageField(required=False)
    
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'role', 'email', 'image']

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Password'
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirm Password'
    )
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields must match.")
        return password2

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

