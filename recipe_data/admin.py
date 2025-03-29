from django.contrib import admin
from .models import Meal
# Register your models here.
@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display=['user','recipe_title','calories','protein','fat','carbs','created_at']
    search_fields=['user','recipe_title']