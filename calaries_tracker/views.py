from django.shortcuts import render
from .forms import CalorieCalculatorForm
from django.contrib import messages
from .utils import get_logged_in_user_email
from user_auth.models import Profile

def calculate_calories(request):
    bmr, tdee = None, None
    print("email=",get_logged_in_user_email(request))
    get_logged_in_user_email(request)
    # messages.info(request, "save your profile to calculate calories")
    if request.method == "POST":
        form = CalorieCalculatorForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data["weight"]
            height = form.cleaned_data["height"]
            age = form.cleaned_data["age"]
            gender = form.cleaned_data["gender"]
            activity_level = form.cleaned_data["activity_level"]

            # BMR Calculation
            if gender == "male":
                bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
            else:
                bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

            # Activity Level Multiplier
            activity_multipliers = {
                "sedentary": 1.2,
                "light": 1.375,
                "moderate": 1.55,
                "active": 1.725,
                "very_active": 1.9,
            }
            tdee = bmr * activity_multipliers.get(activity_level, 1.2)

        if "Save" in request.POST:
            try:
                user=Profile.objects.get(user__email=get_logged_in_user_email(request))
                user.bmr=bmr
                user.calories=tdee
                user.save()
                messages.success(request, f"Profile {user} saved successfully")
            except:
                pass
            

    else:
        profile=Profile.objects.get(user=request.user)
        weight=profile.weight
        height=profile.height
        age=profile.age
        gender=profile.get_gender_display()
        print("\n\n\n\n\n\n\n\nweight=",weight)
        print("height=",height)
        print("age=",age)
        print("gender",gender)
        if profile:
           print("profile=",profile)
           form = CalorieCalculatorForm(initial={
               "age": age,
               "weight": weight,
               "height": height,
               "gender":gender

           })
           print("form=",form)
        else:
            print("profile not found")
            form = CalorieCalculatorForm() 
        # form = CalorieCalculatorForm()

    return render(request, "calculator_form.html", {"form": form, "bmr": bmr, "tdee": tdee})
