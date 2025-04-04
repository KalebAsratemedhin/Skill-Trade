from rest_framework import serializers
from users.serializers import UserSerializer
from .models import JobPosting, JobApplication

class JobPostingSerializer(serializers.ModelSerializer):
    customer = UserSerializer()

    class Meta:
        model = JobPosting
        fields = "__all__"

class CreateJobPostingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = JobPosting
        fields = "__all__"

class UpdateJobPostingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = JobPosting
        fields = ("id","title", "skills", "budget", "description", "location")

class JobApplicationSerializer(serializers.ModelSerializer):
    technician = UserSerializer()

    class Meta:
        model = JobApplication
        fields = "__all__"

class CreateJobApplicationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = JobApplication
        fields = "__all__"

class UpdateJobApplicationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = JobApplication
        fields = ("id", "cover_letter")
