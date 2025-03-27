from users.serializers import CustomerSerializer, TechnicianSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Booking, User

class BookingSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    technician = TechnicianSerializer()

    class Meta:
        model = Booking
        fields = ("__all__")

    
class CreateBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ("id","technician", "date", "time", "service", "customer", "technician")


    def create(self, validated_data):
        return Booking.objects.create(**validated_data)

class UpdateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("id","technician", "date", "time")
    
# class BookingStatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = ("id","status")
