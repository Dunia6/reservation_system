import { defineStore } from 'pinia'
import { ref } from 'vue'
import { apiFetch } from '@/services/apiService'

export const useReservationStore = defineStore('reservation', () => {
  // State
  const loading = ref(false)
  const error = ref(null)
  const reservations = ref([])
  const currentReservation = ref(null)

  // Actions
  async function createReservation(reservationData) {
    loading.value = true
    error.value = null

    try {
      console.log('📤 Envoi de la réservation:', reservationData)
      
      const data = await apiFetch('/api/reservations/', {
        method: 'POST',
        body: JSON.stringify(reservationData)
      })

      console.log('✅ Réservation créée:', data)
      return data

    } catch (err) {
      console.error('❌ Erreur création réservation:', err)
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function reservationsFetch() {
    loading.value = true
    error.value = null

    try {
        reservations.value = await apiFetch('/api/reservations/')
        console.log('✅ Réservations récupérées:', reservations.value)
    } catch (err) {
        console.error("❌ Erreur lors de la récupération des réservations :", err);
        error.value = err.message
        throw err;
    } finally {
        loading.value = false
    }
  }

  async function getReservationById(id) {
    loading.value = true
    error.value = null

    try {
      console.log('📤 Récupération de la réservation ID:', id)
      
      const data = await apiFetch(`/api/reservations/${id}/`)
      currentReservation.value = data

      console.log('✅ Réservation récupérée:', data)
      return data

    } catch (err) {
      console.error('❌ Erreur récupération réservation:', err)
      error.value = err.message
      currentReservation.value = null
      throw err
    } finally {
      loading.value = false
    }
  }

  async function changeRoom(payload) {
    loading.value = true
    error.value = null

    try {
      console.log('📤 Échange de chambre:', payload)
      
      const data = await apiFetch('/api/reservations/change-room/', {
        method: 'POST',
        body: JSON.stringify(payload)
      })

      console.log('✅ Échange effectué:', data)
      
      // Mettre à jour la réservation actuelle si c'est celle-ci qui a été modifiée
      if (currentReservation.value && currentReservation.value.id === payload.reservation_id) {
        await getReservationById(payload.reservation_id)
      }
      
      return data

    } catch (err) {
      console.error('❌ Erreur lors de l\'échange:', err)
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }


  function clearError() {
    error.value = null
  }

  return {
    // State
    loading,
    error,
    reservations,
    currentReservation,
    
    // Actions
    createReservation,
    reservationsFetch,
    getReservationById,
    changeRoom,
    clearError,
  }
})
