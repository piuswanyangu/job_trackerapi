from rest_framework import serializers
from .models import ApplicationAnalytics, JobApplication 

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = "__all__"
        read_only_fields = ["id","user", "created_at", "updated_at"]


# -------------------------
# analytics api endpoint
# ------------------
class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationAnalytics
        fields = "__all__"
