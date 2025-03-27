from .models import TechnicianProfile
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework import serializers
from .models import User

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "phone_number", "address", "email", "role", "password")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class TechnicianProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicianProfile
        fields = ("expertise", "experience_years", "available")

class TechnicianSerializer(serializers.ModelSerializer):
    technician_profile = TechnicianProfileSerializer(required=False)
    class Meta:
        model = User
        fields = ("id", "username", "phone_number", "address", "email", "role", "password", "technician_profile")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        technician_data = validated_data.pop("technician_profile", None) 
        user = User.objects.create_user(**validated_data)
        TechnicianProfile.objects.create(user=user, **technician_data)

        return user
    
    


class UpdateCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phone_number", "address")

class UpdateTechnicianSerializer(serializers.ModelSerializer):
    technician_profile = TechnicianProfileSerializer(required=False)
    class Meta:
        model = User
        fields = ("phone_number", "address", "technician_profile")

    def update(self, instance, validated_data):
        technician_data = validated_data.pop("technician_profile", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        TechnicianProfile.objects.update_or_create(user=instance, defaults=technician_data or {})

        return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return {"id": user.id, "username": user.username, "role": user.role}


