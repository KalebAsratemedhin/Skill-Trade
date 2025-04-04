from users.utils import send_verification_email
from .models import EmailVerificationToken, TechnicianProfile
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    expertise = serializers.CharField(source="technicianprofile.expertise", required=False)
    experience = serializers.IntegerField(source="technicianprofile.experience", required=False)
    available = serializers.BooleanField(source="technicianprofile.available", required=False)

    class Meta:
        model = User
        fields = ("id", "username", "phone_number", "address", "email", "role", "password", "is_verified", "experience", "expertise", "available")

        extra_kwargs = {
            "password": {"write_only": True},
            "is_verified": {"read_only": True}
        }

    def create(self, validated_data):
        technician_data = validated_data.pop("technicianprofile")
        user = User.objects.create_user(**validated_data)

        if user.role == "technician":
            TechnicianProfile.objects.create(user=user, **technician_data)

        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {key: value for key, value in data.items() if value is not None}

class UpdateUserSerializer(serializers.ModelSerializer):
    expertise = serializers.CharField(source="technicianprofile.expertise", required=False)
    experience = serializers.IntegerField(source="technicianprofile.experience", required=False)
    available = serializers.BooleanField(source="technicianprofile.available", required=False)

    class Meta:
        model = User
        fields = ("phone_number", "address", "experience", "expertise", "available")

    def update(self, instance, validated_data):
        technician_data = validated_data.pop("technicianprofile")


        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if instance.role == "technician":
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


