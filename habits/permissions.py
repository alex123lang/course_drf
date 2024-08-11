from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Checks if the user is the owner of the object."""

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False
