from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile
from .models import PatientRegistration
class SignupForm(forms.Form):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES)
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput(), min_length=6)
    specialization = forms.CharField(max_length=100, required=False)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()  # ensure lowercase
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise ValidationError("Phone must contain only digits")
        if len(phone) != 10:
            raise ValidationError("Phone number must be exactly 10 digits")
        return phone

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'age', 'gender', 'department', 'doctor', 'address']
class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = PatientRegistration
        fields = '__all__'
        
        