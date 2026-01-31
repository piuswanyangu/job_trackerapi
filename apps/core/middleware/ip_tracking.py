import socket
from apps.core.tasks import log_request

class IPTrackingMiddleware:
    def __init__(self, get_response):  # Fixed typo: __ini__ -> __init__
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request) # Fixed: matched the method name below
        log_request.delay(ip, request.path, request.method)
        request.client_ip = ip
        return self.get_response(request)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")