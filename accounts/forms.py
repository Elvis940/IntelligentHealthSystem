from django import forms
import cloudinary.uploader
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Account


class UserRegistrationForm(UserCreationForm):
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
        }),
        help_text="Upload a profile picture (optional, max 5MB)"
    )
    
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'role', 'profile_picture']
    
    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            # Validate file size (max 5MB)
            if profile_picture.size > 5 * 1024 * 1024:
                raise ValidationError("Image file too large ( > 5MB )")
            
            # Validate file type
            valid_types = ['image/jpeg', 'image/png']
            if profile_picture.content_type not in valid_types:
                raise ValidationError("Unsupported file type. Please upload a JPEG or PNG image.")
        return profile_picture
    
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

