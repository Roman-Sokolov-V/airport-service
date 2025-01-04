from rest_framework import permissions

class IsAdminAllOrAuthenticatedReadOnly(permissions.BasePermission):
    """
    The request is authenticated as an admin,
     or request is authenticated as user is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS and request.user.is_authenticated or
            request.user.is_staff
        )