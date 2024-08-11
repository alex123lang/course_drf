from rest_framework import permissions


class IsUserOwner(permissions.BasePermission):
    """Check if user is owner of object"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        return False


class IsSuperuserOrStaff(permissions.BasePermission):
    """Check if user is superuser or staff"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user.is_staff
