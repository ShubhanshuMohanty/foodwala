from django.urls import path
from .views import calculate_calories

urlpatterns = [
    path("calories/", calculate_calories, name="calculate_calories"),
]
