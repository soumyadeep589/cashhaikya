from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["create", "partial_update", "delete", "close", "history", "active", "list"]:
            return request.user.is_authenticated
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user:
            return True
        return False
