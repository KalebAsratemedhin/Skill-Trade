from django.db import models
from users.models import User

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    technician = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    service = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("completed", "Completed")], default="pending")

    def __str__(self):
        return f"{self.service} - {self.customer} to {self.technician}"
