from django.urls import path
from .views import (
    JobPostingListCreate,
    JobPostingDetail,
    JobApplicationListView,
    JobApplicationDetailView,
    JobApplicationListForJob,
    TechnicianApplications
)

urlpatterns = [
    path("jobs", JobPostingListCreate.as_view(), name="job-list-create"),
    path("jobs/<int:pk>", JobPostingDetail.as_view(), name="job-detail"),

    path("applications", JobApplicationListView.as_view(), name="job-application-create"),
    path("applications/<int:pk>", JobApplicationDetailView.as_view(), name="job-application-detail"),
    
    path("jobs/<int:pk>/applications", JobApplicationListForJob.as_view(), name="job-applications-list"),
    path("my-applications", TechnicianApplications.as_view(), name="technician-applications"),
]
