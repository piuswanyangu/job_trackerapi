
from django.db import models
from django.conf import settings

# -----------------------------
# application model
# --------------------------------------
class JobApplication(models.Model):
    STATUS_CHOICES = [
        ("applied", "Applied"),
        ("interview", "Interview"),
        ("rejected", "Rejected"),
        ("accepted", "Accepted"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="applied")
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # for IP tracking

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


# -----------------------
# application analytics
# ------------------
class ApplicationAnalytics(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    total_applications = models.IntegerField(default=0)
    applied = models.IntegerField(default=0)
    interviewed = models.IntegerField(default=0)
    offer = models.IntegerField(default=0)
    rejected = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} analytics"