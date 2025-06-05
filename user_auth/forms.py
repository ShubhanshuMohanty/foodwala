from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # aapke custom model ka import

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        }


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))

class ProfileForm(forms.Form):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}))
    weight = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your weight'}))
    height = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your height'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your age'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())

    # Field-specific validation
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) != 10:
            raise forms.ValidationError("Phone number must be 10 digits.")
        return phone

    def clean_weight(self):
        weight = self.cleaned_data['weight']
        if weight <= 0:
            raise forms.ValidationError("Weight must be a positive number.")
        return weight

    def clean_height(self):
        height = self.cleaned_data['height']
        if height <= 0:
            raise forms.ValidationError("Height must be a positive number.")
        return height

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 0 or age > 120:
            raise forms.ValidationError("Enter a valid age between 0 and 120.")
        return age
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if any(char.isdigit() for char in name):
            raise forms.ValidationError("Name should not contain numbers.")
        return name
    

    # Optional: cross-field validation
    def clean(self):
        cleaned_data = super().clean()
        height = cleaned_data.get("height")
        weight = cleaned_data.get("weight")

        if height and weight and weight / ((height / 100) ** 2) > 100:
            raise forms.ValidationError("BMI seems unrealistic. Please recheck height and weight.")
