# from users.serializers import UserSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Booking, User

class BookingSerializer(serializers.ModelSerializer):
    # customer =(read_only=True)  
    # technician = UserSerializer(read_only=True) 

    class Meta:
        model = Booking
        fields = ("__all__")

    
class CreateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("technician", "date", "time", "service")

    def create(self, validated_data):
        return Booking.objects.create(**validated_data)

class UpdateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("technician", "date", "time", "service")
    

    