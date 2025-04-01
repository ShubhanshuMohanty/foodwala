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
    

class premium_member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Kis user ka meal hai
    # start_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    amount=models.FloatField(null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} "
