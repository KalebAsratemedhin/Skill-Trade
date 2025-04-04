from django.db import models
from users.models import User

class JobPosting(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobpostings")
    title = models.CharField(max_length=255)
    skills = models.CharField(max_length=255)
    budget = models.FloatField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[("open", "Open"), ("closed", "Closed")], default="open")

    def __str__(self):
        return self.title
    
class JobApplication(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name="applications")
    technician = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField()
    status = models.CharField(
        max_length=20, 
        choices=[("pending", "Pending"), ("viewed", "Viewed"), ("interviewing", "Interviewing"), ("hired", "Hired")], 
        default="pending"
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.technician.username} - {self.job.title}"
