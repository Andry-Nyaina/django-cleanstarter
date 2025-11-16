from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Permission qui autorise uniquement les admins (is_staff).
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsSelf(permissions.BasePermission):
    """
    Permission : l'utilisateur doit être lui-même.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsAdminOrSelf(permissions.BasePermission):
    """
    Admin → accès illimité
    User normal → accès uniquement à son propre profil
    """
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return obj == request.user


class DenyDeleteSelf(permissions.BasePermission):
    """
    Interdit de supprimer son propre compte.
    """
    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE" and obj == request.user:
            return False
        return True
