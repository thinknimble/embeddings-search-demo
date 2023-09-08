from rest_framework import permissions


class CreateOnlyPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            return True
        return False
