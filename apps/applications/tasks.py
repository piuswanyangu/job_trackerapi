from celery import shared_task
from .models import JobApplication
from django.core.cache import cache

@shared_task
def cache_job_applications(user_id):
    applications = list(JobApplication.objects.filter(user_id=user_id).values())
    cache.set(f"user_apps_{user_id}", applications, timeout=3600)