from django.urls import path
from .views import register_view, login_view, logout_view,create_profile,profile_view,generate_pdf

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create_profile/', create_profile, name='create_profile'),
    path('profile/', profile_view, name='profile'),
    path('pdf/', generate_pdf, name='generate_pdf'),
]
