import { API_BASE_URL } from '@/config/api'
import { useAuthStore } from '@/stores/authStore'

export async function apiFetch(endpoint, options = {}) {
  const authStore = useAuthStore()

  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  }

  if (authStore.accessToken)
    headers['Authorization'] = `Bearer ${authStore.accessToken}`

  let response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  })

  // Si le token est expiré
  if (response.status === 401) {
    try {
      await authStore.refreshAccessToken()
      headers['Authorization'] = `Bearer ${authStore.accessToken}`
      response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
      })
    } catch (error) {
      authStore.logout()
      throw new Error('Session expirée')
    }
  }

  if (!response.ok) {
    const text = await response.text()
    throw new Error(text || `Erreur ${response.status}`)
  }

  return response.json()
}
