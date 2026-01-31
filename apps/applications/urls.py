from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Import your ACTUAL views here
from .views_analytics import DashboardAnalyticsAPIView 

router = DefaultRouter()
# Only register ViewSets here. If you don't have any yet, leave this empty.
# router.register(r'jobs', JobViewSet) 

urlpatterns = [
    # This includes any routes registered in the router
    path('', include(router.urls)),
    
    # This maps the analytics URL to your specific view
    path('analytics/', DashboardAnalyticsAPIView.as_view(), name='analytics'),
]