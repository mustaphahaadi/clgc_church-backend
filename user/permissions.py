from rest_framework.permissions import BasePermission, AllowAny, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if SAFE_METHODS in request.method:
            return True
        return request.user.is_superuser