from django.contrib import admin

from job_posts.models import JobApplication, JobPosting

# Register your models here.
admin.site.register(JobPosting)
admin.site.register(JobApplication)
