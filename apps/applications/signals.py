# ------------------
# autotriger analyics update
# --------------------

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Application
from .tasks import generate_user_analytics

@receiver([post_save, post_delete], sender=Application)
def update_analytics(sender, instance, **kwargs):
    generate_user_analytics.delay(instance.user_id)
