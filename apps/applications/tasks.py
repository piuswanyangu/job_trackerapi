from celery import shared_task
from prompt_toolkit import Application
from .models import ApplicationAnalytics, JobApplication
from django.core.cache import cache
from django.db.models import Count

@shared_task
def cache_job_applications(user_id):
    applications = list(JobApplication.objects.filter(user_id=user_id).values())
    cache.set(f"user_apps_{user_id}", applications, timeout=3600)
    

# ----------------------
# calculate analytics asynchronously
# -----------------------------
@shared_task
def generate_user_analytics(user_id):
    qs = Application.objects.filter(user_id=user_id)

    stats = qs.values("status").annotate(count=Count("id"))

    data = {
        "applied": 0,
        "interviewed": 0,
        "offer": 0,
        "rejected": 0
    }

    for s in stats:
        data[s["status"]] = s["count"]

    ApplicationAnalytics.objects.update_or_create(
        user_id=user_id,
        defaults={
            "total_applications": qs.count(),
            **data
        }
    )