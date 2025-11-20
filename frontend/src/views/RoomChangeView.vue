<template>
    <!-- Loading State -->
    <div v-if="loading" class="container mx-auto px-6 py-8">
        <div class="max-w-3xl mx-auto text-center">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p class="text-gray-600">Chargement...</p>
        </div>
    </div>

    <div v-else class="container mx-auto px-6 py-8">
        <div class="max-w-3xl mx-auto">
            <div class="bg-white rounded-lg border p-6">
                <h2 class="text-xl font-semibold mb-6">Échange de Chambres</h2>

                <form @submit.prevent="handleSubmit" class="space-y-6">
                    <!-- Chambre Source (Occupée) -->
                    <div class="border-b pb-6">
                        <h3 class="font-medium text-gray-900 mb-3">Chambre Actuelle (Occupée)</h3>
                        <div>
                            <label class="block text-sm text-gray-700 mb-2">Sélectionner la chambre occupée *</label>
                            <select 
                                v-model="formData.old_room_id"
                                @change="onOldRoomChange"
                                class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                                required
                            >
                                <option value="">-- Choisir une chambre occupée --</option>
                                <option 
                                    v-for="room in occupiedRooms" 
                                    :key="room.id" 
                                    :value="room.id"
                                >
                                    Chambre {{ room.number }} - {{ room.type?.name }} (Étage {{ room.floor?.number }})
                                </option>
                            </select>
                        </div>

                        <!-- Détails de la chambre actuelle -->
                        <div v-if="oldRoomDetails" class="mt-4 p-4 bg-gray-50 rounded-lg">
                            <h4 class="font-medium text-sm mb-2 text-gray-700">Détails de la chambre:</h4>
                            <p class="text-sm mb-1"><strong>Numéro:</strong> {{ oldRoomDetails.number }}</p>
                            <p class="text-sm mb-1"><strong>Catégorie:</strong> {{ oldRoomDetails.type?.name }}</p>
                            <p class="text-sm mb-1"><strong>Étage:</strong> {{ oldRoomDetails.floor?.number }}</p>
                            <p class="text-sm mb-1"><strong>Prix:</strong> {{ formatCurrency(oldRoomDetails.type?.price_per_night) }}/jour</p>
                            <p class="text-sm"><strong>Statut:</strong> <span class="text-red-600">Occupée</span></p>
                            
                            <!-- Info de la réservation si disponible -->
                            <div v-if="oldRoomDetails.active_reservation" class="mt-3 pt-3 border-t">
                                <p class="text-sm font-medium text-gray-700 mb-1">Réservation active:</p>
                                <p class="text-sm"><strong>Client:</strong> {{ oldRoomDetails.active_reservation.guest?.name }}</p>
                                <p class="text-sm"><strong>Check-in:</strong> {{ oldRoomDetails.active_reservation.check_in }}</p>
                                <p class="text-sm"><strong>Durée:</strong> {{ oldRoomDetails.active_reservation.number_of_days }} jours</p>
                            </div>
                        </div>
                    </div>

                    <!-- Chambre Destination (Libre) -->
                    <div v-if="formData.old_room_id" class="border-b pb-6">
                        <h3 class="font-medium text-gray-900 mb-3">Nouvelle Chambre (Disponible)</h3>
                        <div>
                            <label class="block text-sm text-gray-700 mb-2">Sélectionner la nouvelle chambre *</label>
                            <select 
                                v-model="formData.new_room_id"
                                @change="onNewRoomChange"
                                class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                                required
                            >
                                <option value="">-- Choisir une chambre disponible --</option>
                                <option 
                                    v-for="room in filteredAvailableRooms" 
                                    :key="room.id" 
                                    :value="room.id"
                                >
                                    Chambre {{ room.number }} - {{ room.type?.name }} (Étage {{ room.floor?.number }}) - {{ formatCurrency(room.type?.price_per_night) }}
                                </option>
                            </select>
                        </div>

                        <!-- Détails de la nouvelle chambre -->
                        <div v-if="newRoomDetails" class="mt-4 p-4 bg-green-50 rounded-lg">
                            <h4 class="font-medium text-sm mb-2 text-green-700">Détails de la nouvelle chambre:</h4>
                            <p class="text-sm mb-1"><strong>Numéro:</strong> {{ newRoomDetails.number }}</p>
                            <p class="text-sm mb-1"><strong>Catégorie:</strong> {{ newRoomDetails.type?.name }}</p>
                            <p class="text-sm mb-1"><strong>Étage:</strong> {{ newRoomDetails.floor?.number }}</p>
                            <p class="text-sm mb-1"><strong>Prix:</strong> {{ formatCurrency(newRoomDetails.type?.price_per_night) }}/jour</p>
                            <p class="text-sm"><strong>Statut:</strong> <span class="text-green-600">Disponible</span></p>
                        </div>
                    </div>

                    <!-- Motif -->
                    <div v-if="formData.new_room_id">
                        <label class="block text-sm text-gray-700 mb-2">Motif de l'échange *</label>
                        <textarea 
                            v-model="formData.reason"
                            rows="3" 
                            placeholder="Expliquez la raison de l'échange..." 
                            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                            required
                        ></textarea>
                    </div>

                    <!-- Frais d'échange -->
                    <div v-if="formData.new_room_id">
                        <label class="block text-sm text-gray-700 mb-2">Frais de l'échange</label>
                        <input 
                            v-model.number="formData.exchange_fee"
                            type="number" 
                            placeholder="0" 
                            min="0" 
                            step="0.01" 
                            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                        >

                        <!-- Champs de paiement si frais > 0 -->
                        <div v-if="formData.exchange_fee && formData.exchange_fee > 0" class="mt-4 p-4 bg-yellow-50 rounded-lg space-y-4">
                            <div>
                                <label class="block text-sm text-gray-700 mb-2">Mode de paiement *</label>
                                <select 
                                    v-model="formData.payment_method"
                                    class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                                    required
                                >
                                    <option value="">-- Sélectionner --</option>
                                    <option value="cash">Espèces</option>
                                    <option value="mobile_money">Mobile Money</option>
                                    <option value="credit_card">Carte de Crédit</option>
                                    <option value="bank_transfer">Virement Bancaire</option>
                                    <option value="check">Chèque</option>
                                </select>
                            </div>

                            <div>
                                <label class="block text-sm text-gray-700 mb-2">Référence du paiement</label>
                                <input 
                                    v-model="formData.payment_reference"
                                    type="text" 
                                    placeholder="Référence..." 
                                    class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                                >
                            </div>

                            <div>
                                <label class="block text-sm text-gray-700 mb-2">Notes sur le paiement</label>
                                <textarea 
                                    v-model="formData.payment_notes"
                                    rows="2" 
                                    placeholder="Notes additionnelles..." 
                                    class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                                ></textarea>
                            </div>
                        </div>
                    </div>

                    <!-- Boutons -->
                    <div v-if="formData.new_room_id" class="flex gap-3">
                        <button 
                            type="submit" 
                            :disabled="submitting"
                            class="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:bg-blue-300 disabled:cursor-not-allowed"
                        >
                            {{ submitting ? 'Traitement...' : 'Effectuer l\'échange' }}
                        </button>
                        <button 
                            type="button"
                            @click="handleCancel"
                            class="flex-1 bg-gray-200 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-300 text-center"
                        >
                            Annuler
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { push } from 'notivue'
import { useReservationStore } from '@/stores/reservationStore'
import { useRoomStore } from '@/stores/roomStore'
import { apiFetch } from '@/services/apiService'
import { useCurrency } from '@/composables/useCurrency'

const router = useRouter()
const reservationStore = useReservationStore()
const roomStore = useRoomStore()
const { formatCurrency, loadCompanyInfo } = useCurrency()

const loading = ref(true)
const submitting = ref(false)
const occupiedRooms = ref([])
const availableRooms = ref([])
const oldRoomDetails = ref(null)
const newRoomDetails = ref(null)

const formData = ref({
  reservation_id: '',
  old_room_id: '',
  new_room_id: '',
  reason: '',
  exchange_fee: 0,
  payment_method: '',
  payment_reference: '',
  payment_notes: ''
})

onMounted(async () => {
  try {
    await Promise.all([
      loadCompanyInfo(),
      (async () => {
        // Charger les chambres occupées
        const occupiedData = await apiFetch('/api/rooms/?status=occupied')
        occupiedRooms.value = occupiedData.results || occupiedData
        
        // Charger les chambres disponibles
        const availableData = await apiFetch('/api/rooms/?status=available')
        availableRooms.value = availableData.results || availableData
      })()
    ])
    
    console.log('Chambres occupées:', occupiedRooms.value)
    console.log('Chambres disponibles:', availableRooms.value)
    
    loading.value = false
  } catch (error) {
    console.error('Erreur lors du chargement:', error)
    push.error({
      title: 'Erreur',
      message: 'Impossible de charger les données'
    })
    loading.value = false
  }
})

const onOldRoomChange = async () => {
  oldRoomDetails.value = null
  formData.value.new_room_id = ''
  newRoomDetails.value = null
  formData.value.reservation_id = ''
  
  if (!formData.value.old_room_id) return
  
  try {
    // Charger les détails de l'ancienne chambre (avec active_reservation)
    const room = await apiFetch(`/api/rooms/${formData.value.old_room_id}/`)
    oldRoomDetails.value = room
    
    // Extraire l'ID de la réservation active
    if (room.active_reservation) {
      formData.value.reservation_id = room.active_reservation.id
      console.log('Réservation trouvée:', room.active_reservation)
    } else {
      push.warning({
        title: 'Attention',
        message: 'Cette chambre n\'a pas de réservation active'
      })
    }
  } catch (error) {
    console.error('Erreur:', error)
    push.error({
      title: 'Erreur',
      message: 'Impossible de charger les détails de la chambre'
    })
  }
}

const onNewRoomChange = async () => {
  newRoomDetails.value = null
  
  if (!formData.value.new_room_id) return
  
  try {
    // Charger les détails de la nouvelle chambre
    const room = await apiFetch(`/api/rooms/${formData.value.new_room_id}/`)
    newRoomDetails.value = room
  } catch (error) {
    console.error('Erreur:', error)
    push.error({
      title: 'Erreur',
      message: 'Impossible de charger les détails de la chambre'
    })
  }
}

// Filtrer les chambres disponibles pour exclure la chambre occupée sélectionnée
const filteredAvailableRooms = computed(() => {
  if (!formData.value.old_room_id) return availableRooms.value
  
  // Exclure la chambre actuellement sélectionnée
  return availableRooms.value.filter(room => room.id !== formData.value.old_room_id)
})

const handleSubmit = async () => {
  // Validation
  if (!formData.value.reservation_id || !formData.value.old_room_id || 
      !formData.value.new_room_id || !formData.value.reason) {
    push.warning({
      title: 'Attention',
      message: 'Veuillez remplir tous les champs obligatoires'
    })
    return
  }
  
  if (formData.value.exchange_fee > 0 && !formData.value.payment_method) {
    push.warning({
      title: 'Attention',
      message: 'Veuillez sélectionner un mode de paiement pour les frais d\'échange'
    })
    return
  }
  
  submitting.value = true
  
  try {
    const payload = {
      reservation_id: formData.value.reservation_id,
      old_room_id: formData.value.old_room_id,
      new_room_id: formData.value.new_room_id,
      reason: formData.value.reason
    }
    
    // Ajouter les infos de paiement si un montant est spécifié
    if (formData.value.exchange_fee && formData.value.exchange_fee > 0) {
      payload.exchange_fee = formData.value.exchange_fee
      payload.payment_method = formData.value.payment_method
      
      if (formData.value.payment_reference) {
        payload.payment_reference = formData.value.payment_reference
      }
      if (formData.value.payment_notes) {
        payload.payment_notes = formData.value.payment_notes
      }
    }
    
    const result = await reservationStore.changeRoom(payload)
    
    push.success({
      title: 'Succès',
      message: 'L\'échange de chambre a été effectué avec succès'
    })
    
    // Rediriger vers les détails de la réservation
    router.push(`/reservations/${formData.value.reservation_id}`)
  } catch (error) {
    console.error('Erreur lors de l\'échange:', error)
    push.error({
      title: 'Erreur',
      message: error.message || 'Impossible d\'effectuer l\'échange de chambre'
    })
  } finally {
    submitting.value = false
  }
}

const handleCancel = () => {
  router.push('/reservations')
}
</script>

<style scoped>

</style>
