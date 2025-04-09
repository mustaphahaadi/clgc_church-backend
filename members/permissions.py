from rest_framework.permissions import BasePermission, AllowAny, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if SAFE_METHODS in request.method:
            return True
        return obj.user == request.user or request.user.is_superuser