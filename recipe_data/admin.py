from django.contrib import admin
from .models import Meal,premium_member
# Register your models here.
@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display=['id','user','recipe_title','calories','protein','fat','carbs','created_at']
    search_fields=['user','recipe_title']

@admin.register(premium_member)
class PremiumMemberAdmin(admin.ModelAdmin):
    list_display=['user','start_date','end_date','is_paid','amount']
    search_fields=['user','start_date','end_date','is_paid','amount']
    list_filter=['is_paid']