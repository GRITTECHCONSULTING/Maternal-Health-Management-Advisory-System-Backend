# api/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# ----------------------
# Custom User Model
# ----------------------
class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('provider', 'Healthcare Provider'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username


# ----------------------
# Patient Model
# ----------------------
class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"Patient: {self.user.username}"


# ----------------------
# Provider Model
# ----------------------
class Provider(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100, blank=True)
    license_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Provider: {self.user.username}"


# ----------------------
# Care Category Model
# ----------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
