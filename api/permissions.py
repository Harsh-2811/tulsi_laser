from rest_framework import permissions

class IsTechnicianUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and has the "technician" role.
        return request.user.is_authenticated and request.user.role == "technician"
    