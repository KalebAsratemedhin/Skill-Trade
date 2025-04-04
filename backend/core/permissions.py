from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow only the owner of a profile to update it.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user 
    
class IsTechnician(permissions.BasePermission):
    """
    Allows access only to users with a 'technician' role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "role", None) == "technician"


class IsCustomer(permissions.BasePermission):
    """
    Allows access only to users with a 'customer' role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "role", None) == "customer"