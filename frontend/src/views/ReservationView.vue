<template>
    <div class="container mx-auto px-6 py-8">
        <!-- Page Title -->
        <div class="mb-6">
            <RouterLink to="/" class="text-blue-600 hover:text-blue-800 text-sm font-medium mb-2 inline-block">
                ← Retour
            </RouterLink>
            <h1 class="text-2xl font-bold text-gray-900">Réservation Multiple</h1>
        </div>
        <div class="max-w-6xl mx-auto">
            <!-- Info Banner -->
            <div class="bg-gray-900 text-white p-6 rounded-xl mb-6">
                <div>
                    <h2 class="text-xl font-semibold">Réservation Multiple</h2>
                    <p class="text-gray-300 mt-1">Réservez plusieurs chambres pour un seul client</p>
                </div>
            </div>

            <form @submit.prevent="handleSubmit" class="space-y-6">
                <!-- Informations du Client -->
                <div class="bg-white rounded-xl border border-gray-200 p-6">
                    <h3 class="text-lg font-semibold text-gray-900 mb-4">Informations du Client</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">
                                Nom complet <span class="text-red-500">*</span>
                            </label>
                            <input 
                                type="text" 
                                v-model="form.guest_name"
                                required 
                                placeholder="Ex: Jean Kabongo"
                                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900"
                            >
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">
                                Sexe <span class="text-red-500">*</span>
                            </label>
                            <select 
                                v-model="form.guest_sex"
                                required 
                                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900"
                            >
                                <option value="">-- Sélectionner --</option>
                                <option value="M">Masculin</option>
                                <option value="F">Féminin</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">
                                Type de pièce d'identité <span class="text-red-500">*</span>
                            </label>
                            <select 
                                v-model="form.guest_type_of_id"
                                required 
                                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900"
                            >
                                <option value="">-- Sélectionner --</option>
                                <option value="carte">Carte d'identité</option>
                                <option value="passeport">Passeport</option>
                                <option value="permis">Permis de conduire</option>
                                <option value="autre">Autre</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">
                                Numéro de la pièce <span class="text-red-500">*</span>
                            </label>
                            <input 
                                type="text" 
                                v-model="form.guest_id_number"
                                required 
                                placeholder="Ex: 1-85-00-12345-A-67"
                                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900"
                            >
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">
                                Numéro de téléphone <span class="text-red-500">*</span>
                            </label>
                            <input 
                                type="tel" 
                                v-model="form.guest_contact_number"
                                required
                                placeholder="Ex: +243 900 000 000"
                                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900"
                            >
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">
                                Email (optionnel)
                            </label>
                            <input 
                                type="email" 
                                v-model="form.guest_email"
                                placeholder="Ex: jean@email.com"
                                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900"
                            >
                        </div>
                    </div>
                </div>

                <!-- Période commune -->
                <div class="bg-white rounded-lg border border-gray-200 p-6">
                    <h3 class="text-lg font-semibold text-gray-900 mb-4">Période de Séjour</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">
                                Date d'arrivée <span class="text-red-500">*</span>
                            </label>
                            <input 
                                type="datetime-local" 
                                v-model="form.check_in"
                                required
                                @change="calculateCheckoutDate"
                                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900"
                            >
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">
                                Nombre de jours <span class="text-red-500">*</span>
                            </label>
                            <input 
                                type="number" 
                                v-model.number="form.number_of_days"
                                min="1" 
                                required
                                @input="calculateCheckoutDate"
                                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900"
                            >
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">
                                Date de départ
                            </label>
                            <input 
                                type="date" 
                                v-model="form.check_out_date"
                                readonly
                                class="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 text-gray-600"
                            >
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">
                                Heure de départ
                            </label>
                            <input 
                                type="time" 
                                v-model="form.check_out_time"
                                placeholder="HH:MM"
                                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900"
                            >
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">
                                Nombre de personnes <span class="text-red-500">*</span>
                            </label>
                            <input 
                                type="number" 
                                v-model.number="form.people_count"
                                min="1" 
                                required
                                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900"
                            >
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">
                                Nombre de clés (total) <span class="text-red-500">*</span>
                            </label>
                            <input 
                                type="number" 
                                v-model.number="form.keys_count"
                                min="1" 
                                required
                                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900"
                            >
                        </div>
                    </div>
                </div>

                <!-- Liste des chambres -->
                <div class="bg-white rounded-lg border border-gray-200 p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-semibold text-gray-900">Chambres à réserver</h3>
                        <button 
                            type="button" 
                            @click="addRoom"
                            class="bg-green-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-green-700 transition flex items-center"
                        >
                            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                            </svg>
                            Ajouter une chambre
                        </button>
                    </div>

                    <!-- Liste dynamique des chambres -->
                    <div v-for="(room, index) in selectedRooms" :key="index" class="border-2 border-gray-200 rounded-lg p-4 mb-4">
                        <div class="flex items-center justify-between mb-4">
                            <h4 class="font-bold text-gray-800">Chambre #{{ index + 1 }}</h4>
                            <button 
                                v-if="selectedRooms.length > 1"
                                type="button" 
                                @click="removeRoom(index)"
                                class="text-red-600 hover:text-red-800"
                            >
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                                </svg>
                            </button>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">
                                    Sélectionner une chambre <span class="text-red-500">*</span>
                                </label>
                                <select 
                                    v-model="room.room_id"
                                    required 
                                    @change="calculateTotal"
                                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900"
                                >
                                    <option value="">-- Sélectionner --</option>
                                    <option 
                                        v-for="availRoom in availableRooms" 
                                        :key="availRoom.id" 
                                        :value="availRoom.id"
                                    >
                                        Chambre {{ availRoom.number }} - {{ availRoom.type.name }} ({{ formatCurrency(availRoom.type.price_per_night) }}/jour)
                                    </option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Notes (optionnel)</label>
                                <input 
                                    type="text" 
                                    v-model="room.notes"
                                    placeholder="Ex: Vue sur la mer"
                                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900"
                                >
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Récapitulatif financier -->
                <div class="bg-white rounded-lg border border-gray-200 p-6">
                    <h3 class="text-lg font-semibold text-gray-900 mb-4">Récapitulatif Financier</h3>
                    <div class="bg-linear-to-r from-blue-50 to-indigo-100 p-6 rounded-lg border-2 border-blue-200">
                        <div class="space-y-3">
                            <div class="flex justify-between border-b border-blue-200 pb-2">
                                <span class="text-gray-700">Nombre de chambres:</span>
                                <span class="font-semibold text-gray-800">{{ selectedRooms.length }} chambre(s)</span>
                            </div>
                            <div class="flex justify-between border-b border-blue-200 pb-2">
                                <span class="text-gray-700">Durée du séjour:</span>
                                <span class="font-semibold text-gray-800">{{ form.number_of_days }} jour(s)</span>
                            </div>
                            <div class="flex justify-between border-b border-blue-200 pb-2">
                                <span class="text-gray-700 font-semibold">Coût total:</span>
                                <span class="font-bold text-green-700 text-xl">{{ formatCurrency(totalPrice) }}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-700">Montant déposé:</span>
                                <input 
                                    type="number" 
                                    v-model.number="form.paid_amount"
                                    placeholder="0" 
                                    min="0"
                                    :max="totalPrice"
                                    @input="updatePaymentStatus"
                                    class="w-40 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900"
                                >
                            </div>
                            <div v-if="form.paid_amount > 0" class="flex justify-between">
                                <span class="text-gray-700">Mode de paiement:</span>
                                <select 
                                    v-model="form.payment_method"
                                    class="w-40 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900"
                                >
                                    <option value="cash">Espèces</option>
                                    <option value="mobile_money">Mobile Money</option>
                                    <option value="bank_transfer">Virement</option>
                                    <option value="credit_card">Carte</option>
                                    <option value="check">Chèque</option>
                                </select>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-700 font-semibold">Reste à payer:</span>
                                <span class="font-bold text-red-600 text-lg">{{ formatCurrency(remainingAmount) }}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Action Buttons -->
                <div class="bg-white rounded-lg border border-gray-200 p-6">
                    <div class="flex flex-wrap gap-4">
                        <button 
                            type="submit"
                            :disabled="loading || selectedRooms.length === 0 || !selectedRooms.every(r => r.room_id)"
                            class="flex-1 bg-gray-900 text-white py-4 px-6 rounded-lg font-bold text-lg hover:bg-black transition flex items-center justify-center disabled:bg-gray-400 disabled:cursor-not-allowed"
                        >
                            <svg v-if="!loading" class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            {{ loading ? 'Création en cours...' : 'Créer la réservation multiple' }}
                        </button>
                        <RouterLink 
                            to="/"
                            class="bg-red-500 text-white py-4 px-6 rounded-lg font-semibold hover:bg-red-600 transition"
                        >
                            Annuler
                        </RouterLink>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useRoomStore } from '@/stores/roomStore'
import { useReservationStore } from '@/stores/reservationStore'
import { push } from 'notivue'
import { useCurrency } from '@/composables/useCurrency'

const router = useRouter()
const authStore = useAuthStore()
const roomStore = useRoomStore()
const reservationStore = useReservationStore()
const { formatCurrency, loadCompanyInfo } = useCurrency()

// État du formulaire
const form = ref({
  guest_name: '',
  guest_sex: '',
  guest_type_of_id: '',
  guest_id_number: '',
  guest_contact_number: '',
  guest_email: '',
  people_count: 1,
  keys_count: 1,
  check_in: '',
  number_of_days: 1,
  check_out_date: '',
  check_out_time: '',
  paid_amount: 0,
  payment_method: 'cash',
  payment_status: 'unpaid'
})

// Liste des chambres sélectionnées
const selectedRooms = ref([
  { room_id: '', notes: '' }
])

const loading = ref(false)

// Computed
const initials = computed(() => {
  if (!authStore.user?.username) return '?'
  const name = authStore.user.username.toUpperCase()
  return name.slice(0, 2)
})

const availableRooms = computed(() => {
  return roomStore.rooms.filter(room => room.status === 'available')
})

const totalPrice = computed(() => {
  let total = 0
  selectedRooms.value.forEach(selectedRoom => {
    if (selectedRoom.room_id) {
      const room = roomStore.rooms.find(r => r.id === parseInt(selectedRoom.room_id))
      if (room) {
        total += room.type.price_per_night * form.value.number_of_days
      }
    }
  })
  return total
})

const remainingAmount = computed(() => {
  return Math.max(0, totalPrice.value - (form.value.paid_amount || 0))
})

// Fonctions
function addRoom() {
  selectedRooms.value.push({ room_id: '', notes: '' })
}

function removeRoom(index) {
  if (selectedRooms.value.length > 1) {
    selectedRooms.value.splice(index, 1)
    calculateTotal()
  }
}

function calculateTotal() {
  // Le calcul est automatique via computed totalPrice
  updatePaymentStatus()
}

function calculateCheckoutDate() {
  if (form.value.check_in && form.value.number_of_days) {
    const checkInDate = new Date(form.value.check_in)
    const checkOutDate = new Date(checkInDate)
    checkOutDate.setDate(checkOutDate.getDate() + form.value.number_of_days)
    
    // Format: YYYY-MM-DD
    const year = checkOutDate.getFullYear()
    const month = String(checkOutDate.getMonth() + 1).padStart(2, '0')
    const day = String(checkOutDate.getDate()).padStart(2, '0')
    form.value.check_out_date = `${year}-${month}-${day}`
  }
  
  calculateTotal()
}

function updatePaymentStatus() {
  const total = totalPrice.value
  const paid = form.value.paid_amount || 0
  
  if (paid === 0) {
    form.value.payment_status = 'unpaid'
  } else if (paid >= total) {
    form.value.payment_status = 'paid'
  } else {
    form.value.payment_status = 'partial'
  }
}

async function handleSubmit() {
  try {
    loading.value = true

    // Validation
    if (selectedRooms.value.length === 0) {
      push.warning({
        message: 'Veuillez sélectionner au moins une chambre',
        duration: 4000
      });
      return
    }

    const hasEmptyRoom = selectedRooms.value.some(room => !room.room_id)
    if (hasEmptyRoom) {
      push.warning({
        message: 'Veuillez sélectionner toutes les chambres',
        duration: 4000
      });
      return
    }

    if (form.value.paid_amount > totalPrice.value) {
      push.warning({
        message: 'Le montant déposé ne peut pas dépasser le prix total',
        duration: 4000
      });
      return
    }

    // Préparer les données conformes au backend
    const reservationData = {
      guest_name: form.value.guest_name,
      guest_sex: form.value.guest_sex,
      guest_type_of_id: form.value.guest_type_of_id,
      guest_id_number: form.value.guest_id_number,
      guest_contact_number: form.value.guest_contact_number,
      guest_email: form.value.guest_email || '',
      people_count: form.value.people_count,
      keys_count: form.value.keys_count,
      check_in: form.value.check_in,
      number_of_days: form.value.number_of_days,
      check_out_date: form.value.check_out_date || null,
      check_out_time: form.value.check_out_time || null,
      paid_amount: form.value.paid_amount || 0,
      payment_method: form.value.payment_method || 'cash',
      payment_status: form.value.payment_status,
      rooms: selectedRooms.value.map(room => ({
        room_id: parseInt(room.room_id),
        notes: room.notes || ''
      }))
    }

    // Utiliser le store pour créer la réservation
    const result = await reservationStore.createReservation(reservationData)

    if (result) {
      

        console.log('✅ Réservation multiple créée:', result)

        push.success({
            message: `Réservation créée avec succès ! ${selectedRooms.value.length} chambre(s) réservée(s).`,
            duration: 4000
        });

        // Recharger les chambres
        await roomStore.fetchRooms()
        await reservationStore.getReservationById(result.id)

        // Redirection après 1 seconde
        setTimeout(() => {
            router.push('/invoices/' + result?.id)
        }, 1000)

    }
    
    
    
    

  } catch (error) {
    console.error('❌ Erreur:', error)
    push.error({
      message: error.message || 'Une erreur est survenue',
      duration: 5000
    });
  } finally {
    loading.value = false
  }
}

// Initialisation
onMounted(async () => {
  console.log('🔄 Chargement des chambres disponibles...')
  await Promise.all([
    roomStore.fetchRooms(),
    loadCompanyInfo()
  ])
  
  // Date/heure par défaut
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  
  form.value.check_in = `${year}-${month}-${day}T${hours}:${minutes}`
})
</script>

<style>

</style>