from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.cache import cache

from .models import ApplicationAnalytics
from .serializers import AnalyticsSerializer

class DashboardAnalyticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cache_key = f"analytics_{request.user.id}"
        cached = cache.get(cache_key)

        if cached:
            return Response(cached)

        # This will fetch the record OR create a new one if it's missing
        analytics, created = ApplicationAnalytics.objects.get_or_create(
            user=request.user
        )
        
        data = AnalyticsSerializer(analytics).data
        cache.set(cache_key, data, timeout=300)

        return Response(data)