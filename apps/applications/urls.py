from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.applications.views import JobApplicationViewSet

from .views_analytics import DashboardAnalyticsAPIView 

router = DefaultRouter()
router.register(r'applications', JobApplicationViewSet, basename='job-application')

urlpatterns = [
    path('analytics/', DashboardAnalyticsAPIView.as_view(), name='analytics'),
    # This includes any routes registered in the router
    path('', include(router.urls)),
    

    
]