from rest_framework import permissions


class IsSafeRequest(permissions.BasePermission):
    def has_permission(self, request, view):
        authorization = request.META.get("HTTP_AUTHORIZATION")
        if authorization and authorization == "herren-recruit-python":
            return True

        return False
