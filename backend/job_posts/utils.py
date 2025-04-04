
from job_posts.models import JobApplication, JobPosting


def is_job_posting_duplicate(current):
        
    existing = JobPosting.objects.filter(
                customer=current["customer"],
                location=current["location"],
                description=current["description"],
                budget=current["budget"]
            )

    return existing.exists()

def is_job_application_duplicate(current):
    existing = JobApplication.objects.filter(
            technician=current["technician"],
            job=current["job"]
        )

    return existing.exists()