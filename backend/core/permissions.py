from rest_framework import permissions


class IsReceptionniste(permissions.BasePermission):
    """
    Permission pour vérifier si l'utilisateur est Receptionniste.
    """
    def has_permission(self, request, view):
        return (request.user and 
                request.user.is_authenticated and 
                hasattr(request.user, 'profile') and 
                request.user.profile.role == 'Receptionniste')


class IsManager(permissions.BasePermission):
    """
    Permission pour vérifier si l'utilisateur est Manager.
    """
    def has_permission(self, request, view):
        return (request.user and 
                request.user.is_authenticated and 
                hasattr(request.user, 'profile') and 
                request.user.profile.role == 'Manager')


class IsSuperviseur(permissions.BasePermission):
    """
    Permission pour vérifier si l'utilisateur est Superviseur.
    """
    def has_permission(self, request, view):
        return (request.user and 
                request.user.is_authenticated and 
                hasattr(request.user, 'profile') and 
                request.user.profile.role == 'Superviseur')


class IsManagerOrSuperviseur(permissions.BasePermission):
    """
    Permission pour vérifier si l'utilisateur est Manager OU Superviseur.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        
        if not hasattr(request.user, 'profile'):
            return False
        
        return request.user.profile.role in ['Manager', 'Superviseur']