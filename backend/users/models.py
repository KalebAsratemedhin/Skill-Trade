from django.utils import timezone
import secrets
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.db import models
from django.contrib.auth import get_user_model

class User(AbstractUser):
    ROLE_CHOICES = [
        ("customer", "Customer"),
        ("technician", "Technician"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Customer")
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)

    def generate_email_token(self):
        token = secrets.token_urlsafe(16)
        verification_token = EmailVerificationToken.objects.create(user=self, token=token)
        return verification_token.token
    

class TechnicianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="technicianprofile")
    expertise = models.CharField(max_length=255, blank=True, null=True)
    experience = models.PositiveIntegerField(blank=True, null=True)
    available = models.BooleanField(default=True)

class EmailVerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def is_expired(self):
        return timezone.now() - self.created_at > timezone.timedelta(hours=1) 