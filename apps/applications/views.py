from rest_framework import viewsets, permissions
from rest_framework.response import Response

from apps.applications.tasks import cache_job_applications
from .models import JobApplication
from .serializers import JobApplicationSerializer

class JobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # only return applications for the logged in user
        return JobApplication.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # save user and IP address automatically
        ip = self.get_client_ip()
        app_instance = serializer.save(user=self.request.user, ip_address=ip)
        cache_job_applications.delay(self.request.user.id)

    def get_client_ip(self):
        request = self.request
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.spilt(",")[0]
        else:
            ip = request.META.get("REMOTE_ADR")
        return ip