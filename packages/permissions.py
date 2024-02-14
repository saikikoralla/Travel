from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_superuser)

class IsAdmin_Obj(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_superuser)
    
    def has_object_permissions(self,request,view,obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.username==request.user
