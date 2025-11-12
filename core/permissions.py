from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Lecture (GET, HEAD, OPTIONS) autorisée à tous.
    Modification (POST, PUT, PATCH, DELETE) réservée aux admins (is_staff).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permet la lecture à tous (ou aux utilisateurs authentifiés si on combine),
    mais autorise modification/suppression uniquement au propriétaire de l'objet.
    Attendu : l'objet a un attribut `owner` ou `user` référant à l'User.
    """
    def has_object_permission(self, request, view, obj):
        # Lecture autorisée
        if request.method in permissions.SAFE_METHODS:
            return True

        # Si l'objet a un champ 'owner', utilise-le ; sinon essaye 'user'
        owner = getattr(obj, 'owner', None) or getattr(obj, 'user', None)
        if owner is None:
            # Si pas de champ propriétaire, on refuse modification (pour être sûr)
            return False

        return bool(request.user and request.user.is_authenticated and owner == request.user)
