try:
    from celery import shared_task
except ModuleNotFoundError:
    def shared_task(func):
        return func
from .models import RequestLog

@shared_task
def log_request(ip, path, method):
    RequestLog.objects.create(
        ip_address=ip,
        path=path,
        method=method
    )
