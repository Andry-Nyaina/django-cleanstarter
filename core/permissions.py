from rest_framework import permissions

class IsAdminOrSelf(permissions.BasePermission):
    """
    Permission personnalisée :
    - L'utilisateur admin (is_staff=True) peut tout faire.
    - L'utilisateur normal ne peut accéder qu’à son propre profil.
    """

    def has_object_permission(self, request, view, obj):
        # Si admin → accès complet
        if request.user and request.user.is_staff:
            return True
        # Sinon → accès limité à soi-même
        return obj == request.user
