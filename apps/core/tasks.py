from celery import shared_task
from .models import RequestLog

@shared_task
def log_request(ip, path, method):
    RequestLog.objects.create(
        ip_address=ip,
        path=path,
        method=method
    )