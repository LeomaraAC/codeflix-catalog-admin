from rest_framework.permissions import BasePermission
from src.core._shared.infrastructure.auth.jwt_auth_service import JwtAuthService


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get("Authorization", "")
        if not JwtAuthService(token).is_authenticated():
            return False
        return True


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get("Authorization", "")
        if not JwtAuthService(token).has_role("admin"):
            return False
        return True