from rest_framework import viewsets, permissions

from apps.applications.tasks import cache_job_applications, generate_user_analytics
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
        serializer.save(user=self.request.user, ip_address=ip)
        cache_job_applications(self.request.user.id)
        generate_user_analytics(self.request.user.id)

    def perform_update(self, serializer):
        serializer.save()
        cache_job_applications(self.request.user.id)
        generate_user_analytics(self.request.user.id)

    def perform_destroy(self, instance):
        user_id = self.request.user.id
        instance.delete()
        cache_job_applications(user_id)
        generate_user_analytics(user_id)

    def get_client_ip(self):
        request = self.request
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
