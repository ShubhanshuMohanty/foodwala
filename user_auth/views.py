from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomLoginForm, ProfileForm
from .models import Profile as UserProfile,CustomUser
from .middlewares import guest,auth
from calaries_tracker.utils import get_logged_in_user_email
from recipe_data.models import  premium_member
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
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
            pm=premium_member.objects.create(user=user)
            pm.save()
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
    user=None
    try:
        email=get_logged_in_user_email(request)
        user=UserProfile.objects.get(user__email=email)
    except UserProfile.DoesNotExist:
        return redirect('create_profile')

    return render(request,'users/profile.html',{'user':user})

def generate_pdf(request):
    user=UserProfile.objects.get(user=request.user)
    template_path = 'users\pdf_template.html'
    context = {'user':user}

    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename="my_pdf.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response