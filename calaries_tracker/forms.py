from django import forms
from .utils import get_logged_in_user_email

class CalorieCalculatorForm(forms.Form):
    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]
    ACTIVITY_CHOICES = [
        ("sedentary", "Sedentary (No exercise)"),
        ("light", "Light (1-3 days/week)"),
        ("moderate", "Moderate (3-5 days/week)"),
        ("active", "Active (6-7 days/week)"),
        ("very_active", "Very Active (Athlete)"),
    ]

    weight = forms.FloatField(
        label="Weight (kg)",
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter your weight"})
    )
    height = forms.FloatField(
        label="Height (cm)",
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter your height"})
    )
    age = forms.IntegerField(
        label="Age",
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter your age"})
    )
    gender = forms.ChoiceField(
        label="Gender",
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    activity_level = forms.ChoiceField(
        label="Activity Level",
        choices=ACTIVITY_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"})
    )
