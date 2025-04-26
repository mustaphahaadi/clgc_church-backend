from rest_framework.permissions import BasePermission, AllowAny, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user
        )
    
    def has_object_permission(self, request, view, obj):
        return bool(
            obj.email == request.user.email or
            obj.user == request.user or
            obj.author == request.user or 
            request.user.is_superuser 
        )
    

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_superuser or
            request.user.role == "admin"
        )
    
class IsAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view,obj):
        return bool(
            request.user.is_superuser or
            request.user.is_staff or
            obj.role == "admin"
        ) 