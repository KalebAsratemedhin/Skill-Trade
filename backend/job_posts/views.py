from django.shortcuts import get_object_or_404
from core.permissions import IsOwner, IsTechnician
from job_posts.paginators import JobPostPagination, JobApplicationPagination
from job_posts.utils import is_job_application_duplicate, is_job_posting_duplicate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import JobApplication, JobPosting
from .serializers import CreateJobApplicationSerializer, CreateJobPostingSerializer, JobApplicationSerializer, JobPostingSerializer, UpdateJobApplicationSerializer, UpdateJobPostingSerializer


class JobPostingListCreate(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Filter job postings by status (open/closed)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Page number for pagination",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description="Number of items per page",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={200: JobPostingSerializer(many=True)}
    )
    def get(self, request):
        """Retrieve a paginated and filtered list of job postings."""
        job_postings = JobPosting.objects.all()

        # Apply status filter if provided
        status_filter = request.query_params.get('status')
        if status_filter:
            job_postings = job_postings.filter(status=status_filter)

        paginator = JobPostPagination()
        paginated_job_postings = paginator.paginate_queryset(job_postings, request)
        serializer = JobPostingSerializer(paginated_job_postings, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        request_body=CreateJobPostingSerializer,
        responses={201: JobPostingSerializer}
    )
    def post(self, request):
        """Create a new job posting."""
        data = request.data
        data["customer"] = request.user.id
        serializer = CreateJobPostingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            if is_job_posting_duplicate(data):
                return Response({"error": "Duplicate post."},
                                status=status.HTTP_400_BAD_REQUEST)

            job_post = JobPosting.objects.get(id=serializer.data["id"])
            serializer = JobPostingSerializer(job_post)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobPostingDetail(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]

    @swagger_auto_schema(responses={200: JobPostingSerializer})
    def get(self, request, pk):
        """Retrieve a specific job posting by ID."""
        job = get_object_or_404(JobPosting, pk=pk)
        serializer = JobPostingSerializer(job)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UpdateJobPostingSerializer, responses={200: JobPostingSerializer})
    def put(self, request, pk):
        """Update a job posting (only allowed for the owner)."""
        job = get_object_or_404(JobPosting, pk=pk)
        self.check_object_permissions(request, job.customer)

        serializer = UpdateJobPostingSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            job_post = JobPosting.objects.get(id=serializer.data["id"])
            serializer = JobPostingSerializer(job_post)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: "No content"})
    def delete(self, request, pk):
        """Delete a job posting (only allowed for the owner)."""
        job = get_object_or_404(JobPosting, pk=pk)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobApplicationListView(APIView):
    permission_classes = [IsAuthenticated, IsTechnician]

    @swagger_auto_schema(request_body=CreateJobApplicationSerializer, responses={201: JobApplicationSerializer})
    def post(self, request):
        """Submit a job application."""

        data = request.data
        data["technician"] = request.user.id
        serializer = CreateJobApplicationSerializer(data=request.data)

        if serializer.is_valid():

            if is_job_application_duplicate(data):
                return Response({"error": "Duplicate application."},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

            application = JobApplication.objects.get(id=serializer.data["id"])
            serializer = JobApplicationSerializer(application)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobApplicationDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]

    @swagger_auto_schema(responses={200: JobApplicationSerializer})
    def get(self, request, pk):
        """Retrieve a specific job application by ID."""
        application = get_object_or_404(JobApplication, pk=pk)
        serializer = JobApplicationSerializer(application)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=JobApplicationSerializer, responses={200: JobApplicationSerializer})
    def put(self, request, pk):
        """Update a job application (only allowed for the technician who applied)."""
        application = get_object_or_404(JobApplication, pk=pk)
        serializer = UpdateJobApplicationSerializer(application, data=request.data, partial=True)

        if serializer.is_valid():

            if is_job_application_duplicate(request.data):
                return Response({"error": "Duplicate application."},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

            application = JobApplication.objects.get(id=serializer.data["id"])
            serializer = JobApplicationSerializer(application)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: "No content"})
    def delete(self, request, pk):
        """Delete a job application (only allowed for the technician who applied)."""
        application = get_object_or_404(JobApplication, pk=pk)
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobApplicationListForJob(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Page number for pagination",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description="Number of items per page",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={200: JobApplicationSerializer(many=True)}
    )
    def get(self, request, pk):
        """Retrieve all applications for a specific job (only allowed for the job owner)."""
        job = get_object_or_404(JobPosting, pk=pk)
        applications = job.applications.all()

        paginator = JobApplicationPagination()
        paginated_applications = paginator.paginate_queryset(applications, request)
        serializer = JobApplicationSerializer(paginated_applications, many=True)
        return paginator.get_paginated_response(serializer.data)


class TechnicianApplications(APIView):
    permission_classes = [IsAuthenticated, IsTechnician]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Page number for pagination",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description="Number of items per page",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={200: JobApplicationSerializer(many=True)}
    )
    def get(self, request):
        """Retrieve all job applications submitted by the authenticated technician."""
        applications = JobApplication.objects.filter(technician=request.user)

        paginator = JobApplicationPagination()
        paginated_applications = paginator.paginate_queryset(applications, request)
        serializer = JobApplicationSerializer(paginated_applications, many=True)
        return paginator.get_paginated_response(serializer.data)
