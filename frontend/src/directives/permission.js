import { useAuthStore } from '@/stores/authStore'

/**
 * Directive v-permission
 * Usage: v-permission="'canManageRooms'" ou v-permission="['canManageRooms', 'canManageConfig']"
 * 
 * Cache l'élément si l'utilisateur n'a pas la permission spécifiée
 */
export const vPermission = {
  mounted(el, binding) {
    const authStore = useAuthStore()
    const userRole = authStore.user?.profile?.role
    
    if (!userRole) {
      el.style.display = 'none'
      return
    }
    
    const permissions = Array.isArray(binding.value) ? binding.value : [binding.value]
    
    // Mapping des permissions vers les rôles autorisés
    const permissionMap = {
      // Chambres
      'canViewRooms': ['Receptionniste', 'Manager', 'Superviseur'],
      'canManageRooms': ['Manager', 'Superviseur'],
      
      // Réservations
      'canViewReservations': ['Receptionniste', 'Manager', 'Superviseur'],
      'canCreateReservation': ['Receptionniste', 'Manager', 'Superviseur'],
      'canCancelReservation': ['Manager', 'Superviseur'],
      'canChangeRoom': ['Receptionniste', 'Manager', 'Superviseur'],
      
      // Paiements
      'canAddPayment': ['Receptionniste', 'Manager', 'Superviseur'],
      
      // Configuration
      'canManageConfig': ['Manager', 'Superviseur'],
      'canManageCompanyInfo': ['Manager', 'Superviseur'],
      'canManageRoomTypes': ['Manager', 'Superviseur'],
      'canManageFloors': ['Manager', 'Superviseur'],
      
      // Dashboard
      'canAccessDashboard': ['Superviseur'],
      
      // Guests
      'canViewGuests': ['Receptionniste', 'Manager', 'Superviseur']
    }
    
    // Vérifier si l'utilisateur a au moins une des permissions demandées
    const hasPermission = permissions.some(permission => {
      const allowedRoles = permissionMap[permission] || []
      return allowedRoles.includes(userRole)
    })
    
    if (!hasPermission) {
      el.style.display = 'none'
    }
  },
  
  updated(el, binding) {
    // Re-vérifier lors des mises à jour
    vPermission.mounted(el, binding)
  }
}

/**
 * Directive v-role
 * Usage: v-role="'Manager'" ou v-role="['Manager', 'Superviseur']"
 * 
 * Cache l'élément si l'utilisateur n'a pas le rôle spécifié
 */
export const vRole = {
  mounted(el, binding) {
    const authStore = useAuthStore()
    const userRole = authStore.user?.profile?.role
    
    if (!userRole) {
      el.style.display = 'none'
      return
    }
    
    const roles = Array.isArray(binding.value) ? binding.value : [binding.value]
    
    if (!roles.includes(userRole)) {
      el.style.display = 'none'
    }
  },
  
  updated(el, binding) {
    // Re-vérifier lors des mises à jour
    vRole.mounted(el, binding)
  }
}
