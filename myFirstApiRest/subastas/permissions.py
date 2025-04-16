from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrAdmin(BasePermission):
    """
    Permite editar/eliminar solo si el usuario es el creador de la subasta o es admin.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # Aseguramos que `obj` es una subasta con un `auctioneer`
        return getattr(obj, "auctioneer", None) == request.user or request.user.is_staff
