import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: '/',
      name: 'rooms',
      component: () => import('@/views/RoomsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/rooms/:id',
      name: 'room-details',
      props: true,
      component: () => import('@/views/RoomDetailsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/reservation',
      name: 'reservation',
      component: () => import('@/views/ReservationView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/reservations/:id',
      name: 'reservation-detail',
      component: () => import('@/views/ReservationDetailsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/reservations/:id/payment',
      name: 'add-payment',
      props: true,
      component: () => import('@/views/AddPaymentView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/reservations',
      name: 'reservations-list',
      component: () => import('@/views/ReservationsListView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/invoices/:id',
      name: 'invoice',
      component: () => import('@/views/InvoiceView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/hotel-config',
      name: 'hotel-config',
      component: () => import('@/views/HotelConfigView.vue'),
      meta: { requiresAuth: true, permission: 'canManageConfig' }
    },
    {
      path: '/company-edit',
      name: 'company-edit',
      component: () => import('@/views/CompanyEditView.vue'),
      meta: { requiresAuth: true, permission: 'canManageCompanyInfo' }
    },
    {
      path: '/rooms/create',
      name: 'room-create',
      component: () => import('@/views/RoomEditView.vue'),
      meta: { requiresAuth: true, permission: 'canManageRooms' }
    },
    {
      path: '/rooms/:id/edit',
      name: 'room-edit',
      component: () => import('@/views/RoomEditView.vue'),
      meta: { requiresAuth: true, permission: 'canManageRooms' }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: { requiresAuth: true, permission: 'canAccessDashboard' }
    },
    {
      path: '/room-change',
      name: 'room-change',
      component: () => import('@/views/RoomChangeView.vue'),
      meta: { requiresAuth: true }
    },

  ],
})

// Guards de navigation
const publicPaths = ['/login']
let sessionRestoreAttempted = false

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  

  if (!authStore.isAuthenticated && !sessionRestoreAttempted && to.path !== '/login') {
    sessionRestoreAttempted = true
    try {
      const restored = await authStore.initializeSession()
      console.log("Tentative de restauration de session:", restored)
    } catch (error) {
      console.error("Erreur lors de la restauration de session:", error)
    }
  }

  const isAuthenticated = authStore.isAuthenticated
  console.log("Navigation vers:", to.path, "| Authentifié:", isAuthenticated)


  if (to.path === '/login' && isAuthenticated) {
    return next({ name: 'rooms' })
  }


  if (!publicPaths.includes(to.path) && !isAuthenticated) {
    return next({ name: 'login', query: { redirect: to.fullPath } })
  }

  // Vérifier les permissions si la route en nécessite
  if (to.meta.permission && isAuthenticated) {
    const userRole = authStore.user?.profile?.role
    
    // Mapping des permissions vers les rôles autorisés
    const permissionMap = {
      'canManageConfig': ['Manager', 'Superviseur'],
      'canManageCompanyInfo': ['Manager', 'Superviseur'],
      'canManageRooms': ['Manager', 'Superviseur'],
      'canAccessDashboard': ['Superviseur']
    }
    
    const allowedRoles = permissionMap[to.meta.permission] || []
    
    if (!allowedRoles.includes(userRole)) {
      console.warn(`Accès refusé à ${to.path} pour le rôle ${userRole}`)
      // Rediriger vers la page d'accueil avec un message
      return next({ name: 'rooms', query: { unauthorized: true } })
    }
  }

  next()
})



export default router