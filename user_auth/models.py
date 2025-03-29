from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Login with email
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    weight = models.FloatField()
    height = models.FloatField()
    age = models.IntegerField()
    gender=models.CharField(max_length=10,choices=GENDER_CHOICES,default='M')
    bmr=models.FloatField(null=True,default=0)
    calories=models.FloatField(null=True,default=0)

    def __str__(self):
        return self.user.email
    
class Meal_table(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Kis user ka meal hai
    recipe_title = models.CharField(max_length=255)
    calories = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    carbs = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipe_title} - {self.user.username}"

