from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ("customer", "Customer"),
        ("technician", "Technician"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Customer")
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=20)
    

class TechnicianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="technician_profile")
    expertise = models.CharField(max_length=255, blank=True, null=True)
    experience_years = models.PositiveIntegerField(blank=True, null=True)
    available = models.BooleanField(default=True)


