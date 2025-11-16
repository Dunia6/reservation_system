import { computed } from 'vue'
import { useAuthStore } from '@/stores/authStore'

/**
 * Composable pour gérer les permissions basées sur les rôles
 * Synchronisé avec les permissions Django backend
 */
export function usePermissions() {
  const authStore = useAuthStore()
  
  // Récupérer le rôle de l'utilisateur
  const userRole = computed(() => authStore.user?.profile?.role || null)
  
  // Vérifications de rôles
  const isReceptionniste = computed(() => userRole.value === 'Receptionniste')
  const isManager = computed(() => userRole.value === 'Manager')
  const isSuperviseur = computed(() => userRole.value === 'Superviseur')
  
  // Permissions pour les chambres
  const canViewRooms = computed(() => {
    // Tous les utilisateurs authentifiés peuvent voir les chambres
    return !!userRole.value
  })
  
  const canManageRooms = computed(() => {
    // Seuls Manager et Superviseur peuvent créer/modifier/supprimer des chambres
    return isManager.value || isSuperviseur.value
  })
  
  // Permissions pour les réservations
  const canViewReservations = computed(() => {
    // Tous les utilisateurs authentifiés peuvent voir les réservations
    return !!userRole.value
  })
  
  const canCreateReservation = computed(() => {
    // Tous les utilisateurs authentifiés peuvent créer des réservations
    return !!userRole.value
  })
  
  const canCancelReservation = computed(() => {
    // Seuls Manager et Superviseur peuvent annuler des réservations
    return isManager.value || isSuperviseur.value
  })
  
  const canChangeRoom = computed(() => {
    // Tous les utilisateurs authentifiés peuvent faire des échanges de chambres
    return !!userRole.value
  })
  
  // Permissions pour les paiements
  const canAddPayment = computed(() => {
    // Tous les utilisateurs authentifiés peuvent ajouter des paiements
    return !!userRole.value
  })
  
  // Permissions pour la configuration
  const canManageConfig = computed(() => {
    // Seuls Manager et Superviseur peuvent gérer la configuration
    return isManager.value || isSuperviseur.value
  })
  
  const canManageCompanyInfo = computed(() => {
    // Seuls Manager et Superviseur peuvent modifier les infos de l'entreprise
    return isManager.value || isSuperviseur.value
  })
  
  const canManageRoomTypes = computed(() => {
    // Seuls Manager et Superviseur peuvent gérer les types de chambres
    return isManager.value || isSuperviseur.value
  })
  
  const canManageFloors = computed(() => {
    // Seuls Manager et Superviseur peuvent gérer les étages
    return isManager.value || isSuperviseur.value
  })
  
  // Permissions pour le dashboard
  const canAccessDashboard = computed(() => {
    // Seul le Superviseur peut accéder au dashboard et aux statistiques
    return isSuperviseur.value
  })
  
  // Permissions pour les guests
  const canViewGuests = computed(() => {
    // Tous les utilisateurs authentifiés peuvent voir les invités
    return !!userRole.value
  })
  
  // Fonction helper pour vérifier si l'utilisateur a au moins un des rôles spécifiés
  const hasAnyRole = (...roles) => {
    return roles.includes(userRole.value)
  }
  
  // Fonction helper pour vérifier si l'utilisateur a tous les rôles spécifiés
  const hasAllRoles = (...roles) => {
    return roles.every(role => role === userRole.value)
  }
  
  return {
    // Rôles
    userRole,
    isReceptionniste,
    isManager,
    isSuperviseur,
    
    // Permissions Chambres
    canViewRooms,
    canManageRooms,
    
    // Permissions Réservations
    canViewReservations,
    canCreateReservation,
    canCancelReservation,
    canChangeRoom,
    
    // Permissions Paiements
    canAddPayment,
    
    // Permissions Configuration
    canManageConfig,
    canManageCompanyInfo,
    canManageRoomTypes,
    canManageFloors,
    
    // Permissions Dashboard
    canAccessDashboard,
    
    // Permissions Guests
    canViewGuests,
    
    // Helpers
    hasAnyRole,
    hasAllRoles
  }
}
