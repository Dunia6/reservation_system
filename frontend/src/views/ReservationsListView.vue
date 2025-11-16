<template>
    <!-- Loading State -->
    <div v-if="loading" class="container mx-auto px-6 py-20">
        <div class="flex justify-center items-center">
            <div class="text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto mb-4"></div>
                <p class="text-gray-600">Chargement des réservations...</p>
            </div>
        </div>
    </div>

    <div v-else class="container mx-auto px-6 py-8">
        <!-- Filters -->
        <div class="bg-white rounded-xl border border-gray-200 p-6 mb-6">
            <h3 class="text-base font-semibold text-gray-900 mb-4">Filtres</h3>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Statut</label>
                    <select v-model="filters.status" @change="applyFilters" 
                            class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900">
                        <option value="">Tous</option>
                        <option value="pending">En attente</option>
                        <option value="confirmed">Confirmée</option>
                        <option value="checked_in">Client arrivé</option>
                        <option value="checked_out">Client parti</option>
                        <option value="cancelled">Annulée</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Statut paiement</label>
                    <select v-model="filters.payment_status" @change="applyFilters"
                            class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900">
                        <option value="">Tous</option>
                        <option value="unpaid">Non payé</option>
                        <option value="partial">Partiel</option>
                        <option value="paid">Payé</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Rechercher</label>
                    <input v-model="filters.search" @input="applyFilters" type="text" 
                           placeholder="Nom du client..."
                           class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900">
                </div>
                <div class="flex items-end">
                    <button @click="clearFilters" class="w-full bg-gray-100 text-gray-700 px-6 py-2.5 rounded-lg font-medium hover:bg-gray-200 transition">
                        Réinitialiser
                    </button>
                </div>
            </div>
        </div>

        <!-- Summary Stats -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div class="bg-white rounded-xl border border-gray-200 p-5">
                <p class="text-sm text-gray-600">Total Réservations</p>
                <p class="text-3xl font-semibold text-gray-900 mt-2">{{ reservations.length }}</p>
            </div>
            <div class="bg-white rounded-xl border border-gray-200 p-5">
                <p class="text-sm text-gray-600">Réservations Actives</p>
                <p class="text-3xl font-semibold text-green-600 mt-2">{{ activeReservations }}</p>
            </div>
            <div class="bg-white rounded-xl border border-gray-200 p-5">
                <p class="text-sm text-gray-600">À venir</p>
                <p class="text-3xl font-semibold text-amber-600 mt-2">{{ upcomingReservations }}</p>
            </div>
            <div class="bg-white rounded-xl border border-gray-200 p-5">
                <p class="text-sm text-gray-600">Expirées aujourd'hui</p>
                <p class="text-3xl font-semibold text-red-600 mt-2">{{ checkingOutToday }}</p>
            </div>
        </div>

        <!-- Reservations Table -->
        <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <!-- Table Header -->
            <div class="px-6 py-5 border-b border-gray-200 flex items-center justify-between">
                <div>
                    <h3 class="text-base font-semibold text-gray-900">Liste des Réservations</h3>
                    <p class="text-sm text-gray-500 mt-1">Gérez toutes vos réservations</p>
                </div>
                <button @click="createNewReservation" 
                        class="bg-gray-900 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-black transition">
                    + Nouvelle réservation
                </button>
            </div>

            <div v-if="filteredReservations.length === 0" class="p-12 text-center">
                <p class="text-gray-500 text-lg">Aucune réservation trouvée</p>
            </div>
            <div v-else class="overflow-x-auto">
                <table class="w-full">
                    <thead class="bg-gray-900 text-white">
                        <tr>
                            <th class="px-6 py-4 text-left text-sm font-medium">ID</th>
                            <th class="px-6 py-4 text-left text-sm font-medium">Client</th>
                            <th class="px-6 py-4 text-left text-sm font-medium">Chambres</th>
                            <th class="px-6 py-4 text-left text-sm font-medium">Date début</th>
                            <th class="px-6 py-4 text-left text-sm font-medium">Date fin</th>
                            <th class="px-6 py-4 text-left text-sm font-medium">Montant</th>
                            <th class="px-6 py-4 text-left text-sm font-medium">Créé par</th>
                            <th class="px-6 py-4 text-left text-sm font-medium">Statut</th>
                            <th class="px-6 py-4 text-left text-sm font-medium">Paiement</th>
                            <th class="px-6 py-4 text-center text-sm font-medium">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                        <tr v-for="reservation in filteredReservations" :key="reservation.id" 
                            :class="[
                                'transition',
                                isReservationOverdue(reservation) ? 'bg-red-50 hover:bg-red-100' : 'hover:bg-gray-50'
                            ]">
                            <td class="px-6 py-4 text-sm text-gray-900 font-medium">
                                <div class="flex items-center gap-2">
                                    #{{ reservation.id }}
                                    <span v-if="isReservationOverdue(reservation)" 
                                          class="animate-pulse bg-red-500 text-white text-xs px-2 py-0.5 rounded-full font-bold">
                                        🚨 RETARD
                                    </span>
                                </div>
                            </td>
                            <td class="px-6 py-4">
                                <div class="text-sm font-medium text-gray-900">{{ reservation.guest_name }}</div>
                                <div class="text-xs text-gray-500">{{ reservation.people_count }} personne(s)</div>
                            </td>
                            <td class="px-6 py-4">
                                <div class="text-sm font-medium text-gray-900">{{ reservation.rooms_count }} chambre(s)</div>
                                <div class="text-xs text-gray-500">{{ reservation.number_of_days }} jour(s)</div>
                            </td>
                            <td class="px-6 py-4 text-sm text-gray-600">{{ formatDate(reservation.check_in) }}</td>
                            <td class="px-6 py-4">
                                <div class="text-sm text-gray-600">{{ formatDate(reservation.check_out_date) }}</div>
                                <div v-if="isReservationOverdue(reservation)" class="text-xs text-red-600 font-semibold mt-1">
                                    ⚠️ Expiré {{ getOverdueDays(reservation) }}
                                </div>
                            </td>
                            <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ formatCurrency(reservation.total_price) }}</td>
                            <td class="px-6 py-4">
                                <div class="text-sm font-medium text-gray-900">{{ reservation.created_by_username || 'N/A' }}</div>
                                <div class="text-xs text-gray-500">{{ reservation.created_by_role || '-' }}</div>
                            </td>
                            <td class="px-6 py-4">
                                <span :class="['px-3 py-1 rounded-full text-xs font-medium', getStatusClass(reservation.status)]">
                                    {{ getStatusLabel(reservation.status) }}
                                </span>
                            </td>
                            <td class="px-6 py-4">
                                <span :class="['px-3 py-1 rounded-full text-xs font-medium', getPaymentStatusClass(reservation.payment_status)]">
                                    {{ getPaymentStatusLabel(reservation.payment_status) }}
                                </span>
                            </td>
                            <td class="px-6 py-4">
                                <div class="flex justify-center space-x-2">
                                    <RouterLink :to="`/reservations/${reservation.id}`" 
                                                class="bg-gray-900 text-white px-3 py-1.5 rounded-lg hover:bg-black transition text-xs font-medium">
                                        Voir
                                    </RouterLink>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useReservationStore } from '@/stores/reservationStore';
import { useAuthStore } from '@/stores/authStore';
import { onMounted, ref, computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';
import { useCurrency } from '@/composables/useCurrency';

const router = useRouter();
const reservationStore = useReservationStore();
const authStore = useAuthStore();

const { reservations, loading } = storeToRefs(reservationStore);
const { formatCurrency, loadCompanyInfo } = useCurrency();

// Filters
const filters = ref({
    status: '',
    payment_status: '',
    search: ''
});

onMounted(async () => {
    await Promise.all([
        reservationStore.reservationsFetch(),
        loadCompanyInfo()
    ]);
});

// Computed
const initials = computed(() => {
    if (!authStore.user?.username) return '?';
    const name = authStore.user.username.toUpperCase();
    return name.slice(0, 2);
});

const filteredReservations = computed(() => {
    let filtered = reservations.value || [];
    
    // Filter by status
    if (filters.value.status) {
        filtered = filtered.filter(r => r.status === filters.value.status);
    }
    
    // Filter by payment status
    if (filters.value.payment_status) {
        filtered = filtered.filter(r => r.payment_status === filters.value.payment_status);
    }
    
    // Filter by search
    if (filters.value.search) {
        const search = filters.value.search.toLowerCase();
        filtered = filtered.filter(r => 
            r.guest_name.toLowerCase().includes(search) ||
            r.id.toString().includes(search)
        );
    }
    
    return filtered;
});

// Stats
const activeReservations = computed(() => {
    return (reservations.value || []).filter(r => r.status === 'checked_in').length;
});

const upcomingReservations = computed(() => {
    return (reservations.value || []).filter(r => r.status === 'confirmed').length;
});

const checkingOutToday = computed(() => {
    const today = new Date().toDateString();
    return (reservations.value || []).filter(r => {
        if (!r.check_out_date) return false;
        const checkoutDate = new Date(r.check_out_date).toDateString();
        return checkoutDate === today && (r.status === 'checked_in' || r.status === 'confirmed');
    }).length;
});

// Functions
const applyFilters = () => {
    // Filters are applied automatically via computed property
};

const clearFilters = () => {
    filters.value.status = '';
    filters.value.payment_status = '';
    filters.value.search = '';
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

const getStatusLabel = (status) => {
    const labels = {
        'pending': 'En attente',
        'confirmed': 'Confirmée',
        'checked_in': 'Client arrivé',
        'checked_out': 'Client parti',
        'cancelled': 'Annulée'
    };
    return labels[status] || status;
};

const getStatusClass = (status) => {
    const classes = {
        'pending': 'bg-yellow-100 text-yellow-800',
        'confirmed': 'bg-blue-100 text-blue-800',
        'checked_in': 'bg-green-100 text-green-800',
        'checked_out': 'bg-gray-100 text-gray-800',
        'cancelled': 'bg-red-100 text-red-800'
    };
    return classes[status] || 'bg-gray-100 text-gray-800';
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
        'unpaid': 'bg-red-100 text-red-800',
        'partial': 'bg-orange-100 text-orange-800',
        'paid': 'bg-green-100 text-green-800'
    };
    return classes[status] || 'bg-gray-100 text-gray-800';
};

const viewDetails = (id) => {
    router.push(`/reservations/${id}`);
};

const createNewReservation = () => {
    router.push('/reservation');
};

const isReservationOverdue = (reservation) => {
    // Only check for confirmed or checked_in reservations
    if (reservation.status !== 'confirmed' && reservation.status !== 'checked_in') {
        return false;
    }
    
    if (!reservation.check_out_date) return false;
    
    const now = new Date();
    
    // Create checkout datetime
    let checkoutDateTime;
    if (reservation.check_out_time) {
        // If there's a time, use it
        checkoutDateTime = new Date(`${reservation.check_out_date}T${reservation.check_out_time}`);
    } else {
        // If no time, assume end of day (23:59:59)
        checkoutDateTime = new Date(reservation.check_out_date);
        checkoutDateTime.setHours(23, 59, 59, 999);
    }
    
    return now > checkoutDateTime;
};

const getOverdueDays = (reservation) => {
    if (!reservation.check_out_date) return '';
    
    const now = new Date();
    let checkoutDateTime;
    
    if (reservation.check_out_time) {
        checkoutDateTime = new Date(`${reservation.check_out_date}T${reservation.check_out_time}`);
    } else {
        checkoutDateTime = new Date(reservation.check_out_date);
        checkoutDateTime.setHours(23, 59, 59, 999);
    }
    
    const diffMs = now - checkoutDateTime;
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffDays > 0) {
        return `depuis ${diffDays} jour${diffDays > 1 ? 's' : ''}`;
    } else if (diffHours > 0) {
        return `depuis ${diffHours} heure${diffHours > 1 ? 's' : ''}`;
    } else {
        const diffMinutes = Math.floor(diffMs / (1000 * 60));
        return `depuis ${diffMinutes} minute${diffMinutes > 1 ? 's' : ''}`;
    }
};

</script>

<style>

</style>