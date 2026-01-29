from celery import shared_task

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={'max_retries': 3})
def debug_task(self):
    print("🔥 Celery is working correctly")
    return "Celery task executed successfully"
