from django.contrib import admin
from .models import CustomUser,Profile
# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display=['id','email','password','is_active','is_staff','username']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['user','name','phone','weight','height','age','gender','calories','bmr','activity_level']