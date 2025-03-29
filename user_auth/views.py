from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomLoginForm, ProfileForm
from .models import Profile as UserProfile
from .middlewares import guest,auth
from calaries_tracker.utils import get_logged_in_user_email
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('create_profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def create_profile(request):
    if request.method=='POST':
        form=ProfileForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            phone=form.cleaned_data['phone']
            weight=form.cleaned_data['weight']
            height=form.cleaned_data['height']
            age=form.cleaned_data['age']
            user=request.user
            user_profile=UserProfile(user=user,name=name,phone=phone,weight=weight,height=height,age=age)
            user_profile.save()
            return redirect('search')
    else:
        form=ProfileForm()
    return render(request,'users/create_profile.html',{'form':form})

@guest
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # Email used as username
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('search')
    else:
        form = CustomLoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


@auth
def profile_view(request):
    email=get_logged_in_user_email(request)
    user=UserProfile.objects.get(user__email=email)

    return render(request,'users/profile.html',{'user':user})
