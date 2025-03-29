from django.db import models
# from django.contrib.auth.models import User
from user_auth.models import CustomUser as User

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Kis user ka meal hai
    recipe_title = models.CharField(max_length=255)
    calories = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    carbs = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipe_title} "
