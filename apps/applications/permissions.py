from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has__object_permissions(self, request, view, obj):
        return obj.user == request.user