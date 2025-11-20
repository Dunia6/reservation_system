<template>
    <!-- Loading State -->
    <div v-if="loading" class="container mx-auto px-6 py-20">
        <div class="flex justify-center items-center">
            <div class="text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto mb-4"></div>
                <p class="text-gray-600">Chargement des détails...</p>
            </div>
        </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="container mx-auto px-6 py-20">
        <div class="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
            <p class="text-red-600 font-medium mb-4">{{ error }}</p>
            <button @click="goBack" class="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition">
                Retour à la liste
            </button>
        </div>
    </div>

    <!-- Content -->
    <div v-else-if="currentRoom" class="container mx-auto px-6 py-8">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Main Info -->
            <div class="lg:col-span-2 space-y-6">
                <!-- Room Info Card -->
                <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
                    <div class="h-64 bg-linear-to-br from-gray-100 to-gray-200 flex items-center justify-center relative">
                        <span class="text-8xl font-light text-gray-400">{{ currentRoom.number }}</span>
                        <div class="absolute top-4 right-4">
                            <span 
                                :class="[
                                    'px-4 py-2 rounded-full text-sm font-medium',
                                    currentRoom.status === 'available' 
                                        ? 'bg-green-500 text-white' 
                                        : currentRoom.status === 'occupied'
                                        ? 'bg-red-500 text-white'
                                        : 'bg-amber-500 text-white'
                                ]"
                            >
                                {{ 
                                    currentRoom.status === 'available' ? 'Libre' : 
                                    currentRoom.status === 'occupied' ? 'Occupé' : 
                                    'Maintenance' 
                                }}
                            </span>
                        </div>
                    </div>
                    <div class="p-6">
                        <h2 class="text-3xl font-semibold text-gray-900 mb-4">Chambre {{ currentRoom.number }}</h2>
                        <div class="grid grid-cols-2 gap-4">
                            <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
                                <p class="text-sm text-gray-600 mb-1">Niveau</p>
                                <p class="text-xl font-semibold text-gray-800">Niveau {{ currentRoom.floor.number }}</p>
                            </div>
                            <div class="bg-gray-50 p-4 rounded-lg">
                                <p class="text-sm text-gray-600 mb-1">Prix par nuit</p>
                                <p class="text-xl font-semibold text-gray-800">{{ currentRoom.type.price_per_night }} $</p>
                            </div>
                            <div class="bg-gray-50 p-4 rounded-lg">
                                <p class="text-sm text-gray-600 mb-1">Statut</p>
                                <p 
                                    :class="[
                                        'text-xl font-semibold',
                                        currentRoom.status === 'available' ? 'text-green-600' : 
                                        currentRoom.status === 'occupied' ? 'text-red-600' : 
                                        'text-amber-600'
                                    ]"
                                >
                                    {{ 
                                        currentRoom.status === 'available' ? 'Libre' : 
                                        currentRoom.status === 'occupied' ? 'Occupé' : 
                                        'Maintenance' 
                                    }}
                                </p>
                            </div>
                            <div class="bg-gray-50 p-4 rounded-lg">
                                <p class="text-sm text-gray-600 mb-1">Type</p>
                                <p class="text-xl font-semibold text-gray-800">{{ currentRoom.type.name }}</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Guest Information -->
                <div v-if="currentRoom.status === 'occupied' && currentRoom.active_reservation" class="bg-white rounded-xl border border-gray-200 p-6">
                    <h3 class="text-lg font-semibold text-gray-900 mb-4">
                        Informations du Client
                    </h3>
                    <div class="space-y-3">
                        <div class="flex justify-between border-b border-gray-100 pb-2">
                            <span class="text-gray-600">Nom complet</span>
                            <span class="font-medium text-gray-900">{{ currentRoom.active_reservation.guest.name }}</span>
                        </div>
                        <div class="flex justify-between border-b border-gray-100 pb-2">
                            <span class="text-gray-600">Sexe</span>
                            <span class="font-medium text-gray-900">{{ currentRoom.active_reservation.guest.sex }}</span>
                        </div>
                        <div class="flex justify-between border-b border-gray-100 pb-2">
                            <span class="text-gray-600">Type pièce d'identité</span>
                            <span class="font-medium text-gray-900">{{ currentRoom.active_reservation.guest.type_of_id }}</span>
                        </div>
                        <div class="flex justify-between border-b border-gray-100 pb-2">
                            <span class="text-gray-600">Numéro pièce</span>
                            <span class="font-medium text-gray-900">{{ currentRoom.active_reservation.guest.id_number }}</span>
                        </div>
                        <div v-if="currentRoom.active_reservation.guest.contact_number" class="flex justify-between border-b border-gray-100 pb-2">
                            <span class="text-gray-600">Téléphone</span>
                            <span class="font-medium text-gray-900">{{ currentRoom.active_reservation.guest.contact_number }}</span>
                        </div>
                        <div v-if="currentRoom.active_reservation.guest.email" class="flex justify-between border-b border-gray-100 pb-2">
                            <span class="text-gray-600">Email</span>
                            <span class="font-medium text-gray-900">{{ currentRoom.active_reservation.guest.email }}</span>
                        </div>
                    </div>
                </div>

                <!-- Empty State for Available Room -->
                <div v-else class="bg-white rounded-xl border border-gray-200 p-6">
                    <div class="text-center py-8">
                        <p class="text-gray-500 text-lg mb-2">Cette chambre est disponible</p>
                        <p class="text-gray-400 text-sm">Aucune réservation en cours</p>
                    </div>
                </div>

                <!-- Reservation Details -->
                <div v-if="currentRoom.status === 'occupied' && currentRoom.active_reservation" class="bg-white rounded-xl border border-gray-200 p-6">
                    <h3 class="text-lg font-semibold text-gray-900 mb-4">
                        Détails de la Réservation
                    </h3>
                    <div class="space-y-3">
                        <div class="flex justify-between border-b border-gray-100 pb-2">
                            <span class="text-gray-600">Nombre de personnes</span>
                            <span class="font-medium text-gray-900">{{ currentRoom.active_reservation.people_count }} personne(s)</span>
                        </div>
                        <div class="flex justify-between border-b border-gray-100 pb-2">
                            <span class="text-gray-600">Nombre de clés</span>
                            <span class="font-medium text-gray-900">{{ currentRoom.active_reservation.keys_count }} clé(s)</span>
                        </div>
                        <div class="flex justify-between border-b border-gray-100 pb-2">
                            <span class="text-gray-600">Date d'arrivée</span>
                            <span class="font-medium text-gray-900">{{ formatDateTime(currentRoom.active_reservation.check_in) }}</span>
                        </div>
                        <div class="flex justify-between border-b border-gray-100 pb-2">
                            <span class="text-gray-600">Nombre de jours</span>
                            <span class="font-medium text-gray-900">{{ currentRoom.active_reservation.number_of_days }} jour(s)</span>
                        </div>
                        <div v-if="currentRoom.active_reservation.check_out_date" class="flex justify-between border-b border-gray-100 pb-2">
                            <span class="text-gray-600">Date de départ</span>
                            <span class="font-medium text-gray-900">{{ formatDate(currentRoom.active_reservation.check_out_date) }}</span>
                        </div>
                        <div v-if="currentRoom.active_reservation.check_out_time" class="flex justify-between border-b border-gray-100 pb-2">
                            <span class="text-gray-600">Heure de départ</span>
                            <span class="font-medium text-gray-900">{{ currentRoom.active_reservation.check_out_time }}</span>
                        </div>
                        <div class="flex justify-between border-b border-gray-100 pb-2">
                            <span class="text-gray-600">Statut réservation</span>
                            <span :class="getStatusClass(currentRoom.active_reservation.status)">
                                {{ getStatusLabel(currentRoom.active_reservation.status) }}
                            </span>
                        </div>
                        <div class="flex justify-between border-b border-gray-100 pb-2">
                            <span class="text-gray-600">Prix chambre/jour</span>
                            <span class="font-medium text-gray-900">{{ formatCurrency(currentRoom.active_reservation.price_per_day) }}</span>
                        </div>
                        <div class="flex justify-between border-b border-gray-100 pb-2">
                            <span class="text-gray-600">Montant total</span>
                            <span class="font-medium text-gray-900">{{ formatCurrency(currentRoom.active_reservation.total_price) }}</span>
                        </div>
                        <div class="flex justify-between border-b border-gray-100 pb-2">
                            <span class="text-gray-600">Montant déposé</span>
                            <span class="font-semibold text-green-600">{{ formatCurrency(currentRoom.active_reservation.paid_amount) }}</span>
                        </div>
                        <div class="flex justify-between border-b pb-2">
                            <span class="text-gray-600">Statut paiement</span>
                            <span :class="getPaymentStatusClass(currentRoom.active_reservation.payment_status)">
                                {{ getPaymentStatusLabel(currentRoom.active_reservation.payment_status) }}
                            </span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600 font-semibold">Reste à payer</span>
                            <span class="font-semibold text-red-600">{{ formatCurrency(remainingAmount) }}</span>
                        </div>
                        <div v-if="currentRoom.active_reservation.notes" class="pt-2 border-t border-gray-200">
                            <span class="text-gray-600 text-sm">Notes:</span>
                            <p class="text-gray-900 mt-1">{{ currentRoom.active_reservation.notes }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Sidebar Actions -->
            <div class="space-y-6">
                <!-- Room Info Summary for Available Room -->
                <div v-if="currentRoom.status === 'available'" class="bg-white rounded-lg shadow-md p-6">
                    <h3 class="text-lg font-bold text-gray-800 mb-4">Informations</h3>
                    <div class="space-y-4">
                        <div class="bg-linear-to-r from-green-50 to-green-100 p-4 rounded-lg">
                            <p class="text-sm text-green-600 mb-1">Statut</p>
                            <p class="text-2xl font-bold text-green-700">Disponible</p>
                        </div>
                        <div class="bg-linear-to-r from-blue-50 to-blue-100 p-4 rounded-lg">
                            <p class="text-sm text-blue-600 mb-1">Niveau</p>
                            <p class="text-2xl font-bold text-blue-700">{{ currentRoom.floor.number }}</p>
                        </div>
                        <div class="bg-linear-to-r from-purple-50 to-purple-100 p-4 rounded-lg">
                            <p class="text-sm text-purple-600 mb-1">Type</p>
                            <p class="text-xl font-bold text-purple-700">{{ currentRoom.type.name }}</p>
                        </div>
                    </div>
                </div>

                <!-- Actions -->
                <div class="bg-white rounded-lg shadow-md p-6">
                    <h3 class="text-lg font-bold text-gray-800 mb-4">Actions</h3>
                    <div class="space-y-3">
                        <button 
                            v-if="currentRoom.status === 'occupied'"
                            class="block w-full bg-blue-600 text-white text-center py-3 px-4 rounded-lg font-semibold hover:bg-blue-700 transition"
                        >
                        <router-link :to="`/reservations/${currentRoom.active_reservation.id}`" class="w-full h-full block">
                            Voir la réservation
                        </router-link>
                            
                        </button>
                        <button 
                            v-else
                            class="block w-full bg-green-600 text-white text-center py-3 px-4 rounded-lg font-semibold hover:bg-green-700 transition"
                            @click="$router.push('/reservation')"
                            >
                        
                            Faire une réservation
                        </button>
                        <button 
                            @click="goBack"
                            class="block w-full bg-gray-200 text-gray-700 text-center py-3 px-4 rounded-lg font-semibold hover:bg-gray-300 transition"
                        >
                            Retour à la liste
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useRoomStore } from '@/stores/roomStore';
import { onMounted, computed } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';
import { useCurrency } from '@/composables/useCurrency';

const router = useRouter();
const roomStore = useRoomStore();
const authStore = useAuthStore();

const { currentRoom, loading, error } = storeToRefs(roomStore);
const { user } = storeToRefs(authStore);
const { formatCurrency, loadCompanyInfo } = useCurrency();

const props = defineProps({
    id: {
        type: String,
        required: true
    }
});

onMounted(async () => {
    await Promise.all([
        roomStore.getRoomById(props.id),
        loadCompanyInfo()
    ]);
});

const goBack = () => {
    router.push('/');
};

// Computed
const remainingAmount = computed(() => {
    if (!currentRoom.value?.active_reservation) return 0;
    const total = parseFloat(currentRoom.value.active_reservation.total_price);
    const paid = parseFloat(currentRoom.value.active_reservation.paid_amount);
    return Math.max(0, total - paid);
});

// Helper functions
const formatDateTime = (datetime) => {
    if (!datetime) return 'N/A';
    const date = new Date(datetime);
    return date.toLocaleString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
};

const formatDate = (date) => {
    if (!date) return 'N/A';
    const d = new Date(date);
    return d.toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
};

const getStatusLabel = (status) => {
    const labels = {
        'pending': 'En attente',
        'confirmed': 'Confirmée',
        'checked_in': 'Arrivé',
        'checked_out': 'Parti',
        'cancelled': 'Annulée'
    };
    return labels[status] || status;
};

const getStatusClass = (status) => {
    const classes = {
        'pending': 'font-medium text-yellow-600',
        'confirmed': 'font-medium text-blue-600',
        'checked_in': 'font-medium text-green-600',
        'checked_out': 'font-medium text-gray-600',
        'cancelled': 'font-medium text-red-600'
    };
    return classes[status] || 'font-medium text-gray-600';
};

const getPaymentStatusLabel = (status) => {
    const labels = {
        'unpaid': 'Non payé',
        'partial': 'Partiel',
        'paid': 'Payé'
    };
    return labels[status] || status;
};

const getPaymentStatusClass = (status) => {
    const classes = {
        'unpaid': 'font-semibold text-red-600',
        'partial': 'font-semibold text-orange-600',
        'paid': 'font-semibold text-green-600'
    };
    return classes[status] || 'font-semibold text-gray-600';
};

</script>

<style>

</style>