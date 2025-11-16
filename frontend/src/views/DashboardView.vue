<template>
    <div class="container mx-auto px-4 py-8">
        <!-- Page Title -->
        <div class="mb-6">
            <button @click="$router.back()" class="text-blue-600 hover:text-blue-800 text-sm font-medium mb-2 inline-block">
                ← Retour
            </button>
            <h1 class="text-2xl font-bold text-gray-900">Dashboard</h1>
        </div>
        <!-- Statistics Cards - Focus Revenus -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            <!-- Revenus Aujourd'hui -->
            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-600 mb-1">Revenus Aujourd'hui</p>
                        <p class="text-3xl font-bold text-green-700">
                            {{ stats.today ? formatPrice(stats.today.revenue) : formatCurrency(0) }}
                        </p>
                        <p class="text-xs text-gray-600 mt-1">
                            {{ stats.today ? stats.today.reservations : 0 }} réservation(s)
                        </p>
                    </div>
                    <div class="bg-green-100 p-4 rounded-full">
                        <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                </div>
            </div>

            <!-- Revenus Cette Semaine -->
            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-600 mb-1">Revenus Cette Semaine</p>
                        <p class="text-3xl font-bold text-blue-700">
                            {{ stats.week ? formatPrice(stats.week.revenue) : formatCurrency(0) }}
                        </p>
                        <p class="text-xs text-gray-600 mt-1">
                            {{ stats.week ? stats.week.reservations : 0 }} réservation(s)
                        </p>
                    </div>
                    <div class="bg-blue-100 p-4 rounded-full">
                        <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                        </svg>
                    </div>
                </div>
            </div>

            <!-- Revenus Ce Mois -->
            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-yellow-500">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-600 mb-1">Revenus Ce Mois</p>
                        <p class="text-3xl font-bold text-yellow-700">
                            {{ stats.month ? formatPrice(stats.month.revenue) : formatCurrency(0) }}
                        </p>
                        <p class="text-xs text-gray-600 mt-1">
                            {{ stats.month ? stats.month.reservations : 0 }} réservation(s)
                        </p>
                    </div>
                    <div class="bg-yellow-100 p-4 rounded-full">
                        <svg class="w-8 h-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"></path>
                        </svg>
                    </div>
                </div>
            </div>
        </div>

        <!-- Charts & Recent Activities -->
        <div class="mb-8">
            <!-- État d'Occupation Actuel -->
            <div class="bg-white rounded-lg shadow-md p-6">
                <h3 class="text-lg font-bold text-gray-800 mb-4">État d'Occupation Actuel par Niveau</h3>
                
                <!-- Loading State -->
                <div v-if="loadingOccupancy" class="flex justify-center items-center py-12">
                    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
                    <span class="ml-3 text-gray-600">Chargement...</span>
                </div>

                <!-- Empty State -->
                <div v-else-if="!occupancyStats.by_floor || occupancyStats.by_floor.length === 0" class="text-center py-12">
                    <p class="text-gray-600">Aucune donnée d'occupation disponible</p>
                </div>

                <!-- Occupancy Data -->
                <div v-else class="space-y-6">
                    <!-- Floor Stats -->
                    <div v-for="floor in occupancyStats.by_floor" :key="floor.floor_number">
                        <div class="flex justify-between items-center mb-3">
                            <div>
                                <span class="text-gray-800 font-semibold text-lg">{{ floor.floor_name }}</span>
                                <span class="text-gray-500 text-sm ml-2">({{ floor.total_rooms }} chambres)</span>
                            </div>
                            <div class="text-right">
                                <span class="text-2xl font-bold text-red-600">{{ floor.occupied }}</span>
                                <span class="text-gray-500 mx-1">/</span>
                                <span class="text-2xl font-bold text-green-600">{{ floor.available }}</span>
                                <span v-if="floor.maintenance > 0" class="text-gray-500 mx-1">/</span>
                                <span v-if="floor.maintenance > 0" class="text-2xl font-bold text-orange-600">{{ floor.maintenance }}</span>
                            </div>
                        </div>
                        <div class="flex gap-1">
                            <div 
                                v-if="floor.occupied > 0"
                                class="bg-red-500 h-10 rounded flex items-center justify-center text-white text-sm font-semibold" 
                                :style="`flex: ${floor.occupied}`"
                            >
                                Occupées: {{ floor.occupied }}
                            </div>
                            <div 
                                v-if="floor.available > 0"
                                class="bg-green-500 h-10 rounded flex items-center justify-center text-white text-sm font-semibold" 
                                :style="`flex: ${floor.available}`"
                            >
                                Libres: {{ floor.available }}
                            </div>
                            <div 
                                v-if="floor.maintenance > 0"
                                class="bg-orange-500 h-10 rounded flex items-center justify-center text-white text-sm font-semibold" 
                                :style="`flex: ${floor.maintenance}`"
                            >
                                Maintenance: {{ floor.maintenance }}
                            </div>
                        </div>
                    </div>

                    <!-- Total Summary -->
                    <div v-if="occupancyStats.summary" class="pt-4 border-t">
                        <div class="flex justify-between items-center">
                            <span class="text-gray-700 font-semibold">TOTAL ({{ occupancyStats.summary.total_rooms }} chambres)</span>
                            <div>
                                <span class="text-3xl font-bold text-red-600">{{ occupancyStats.summary.occupied }}</span>
                                <span class="text-gray-500 mx-2">/</span>
                                <span class="text-3xl font-bold text-green-600">{{ occupancyStats.summary.available }}</span>
                                <span v-if="occupancyStats.summary.maintenance > 0" class="text-gray-500 mx-2">/</span>
                                <span v-if="occupancyStats.summary.maintenance > 0" class="text-3xl font-bold text-orange-600">{{ occupancyStats.summary.maintenance }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Historique des Paiements -->
        <div class="bg-white rounded-lg shadow-md p-6">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg font-bold text-gray-800">Historique des Paiements</h3>
                <span v-if="!loadingPayments" class="text-sm text-gray-500">{{ payments.length }} entrées</span>
            </div>
            
            <!-- Loading State -->
            <div v-if="loadingPayments" class="flex justify-center items-center py-12">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
                <span class="ml-3 text-gray-600">Chargement...</span>
            </div>

            <!-- Error State -->
            <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
                <p class="text-red-600">{{ error }}</p>
            </div>

            <!-- Empty State -->
            <div v-else-if="payments.length === 0" class="text-center py-12">
                <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <p class="text-gray-600">Aucun paiement enregistré</p>
            </div>

            <!-- Payments List -->
            <div v-else class="space-y-3 max-h-[600px] overflow-y-auto">
                <div 
                    v-for="payment in payments" 
                    :key="payment.id"
                    class="flex items-start space-x-3 pb-3 border-b hover:bg-gray-50 p-3 rounded transition"
                >
                    <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center shrink-0">
                        <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                    <div class="flex-1">
                        <div class="flex justify-between items-start">
                            <div>
                                <p class="text-sm font-semibold text-gray-800">Paiement de {{ formatPrice(payment.amount) }}</p>
                                <p class="text-xs text-gray-600">
                                    {{ payment.guest_name }} - 
                                    <span class="font-medium">Chambre(s): {{ payment.room_numbers.join(', ') }}</span>
                                </p>
                                <div class="flex items-center gap-2 mt-1">
                                    <span class="inline-block bg-purple-100 text-purple-800 px-2 py-0.5 rounded text-xs font-semibold">
                                        {{ payment.payment_method_display }}
                                    </span>
                                    <span v-if="payment.reference_number" class="text-xs text-gray-500">
                                        Réf: {{ payment.reference_number }}
                                    </span>
                                </div>
                                <p v-if="payment.notes" class="text-xs text-gray-700 mt-1 italic bg-gray-50 p-2 rounded">
                                    Note: {{ payment.notes }}
                                </p>
                                <p class="text-xs text-gray-500 mt-1">
                                    {{ formatDateTime(payment.payment_date) }}
                                    <span v-if="payment.created_by_username" class="ml-2">
                                        par <span class="font-medium">{{ payment.created_by_username }}</span>
                                        <span v-if="payment.created_by_role" class="text-gray-400">({{ payment.created_by_role }})</span>
                                    </span>
                                </p>
                            </div>
                            <RouterLink 
                                :to="`/reservations/${payment.reservation_id}`"
                                class="text-blue-600 hover:text-blue-800 text-xs font-medium"
                            >
                                Voir
                            </RouterLink>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import { apiFetch } from '@/services/apiService';
import { push } from 'notivue';
import { useCurrency } from '@/composables/useCurrency';

// State
const payments = ref([]);
const loadingPayments = ref(false);
const error = ref(null);
const stats = ref({
    today: null,
    week: null,
    month: null
});
const occupancyStats = ref({
    by_floor: [],
    summary: null
});
const loadingOccupancy = ref(false);

const { formatCurrency, loadCompanyInfo } = useCurrency();

// Load payments history
const loadPaymentsHistory = async () => {
    loadingPayments.value = true;
    error.value = null;
    
    try {
        const data = await apiFetch('/api/reservations/payments-history/?limit=100');
        payments.value = data;
    } catch (err) {
        error.value = 'Erreur lors du chargement de l\'historique des paiements';
        push.error({
            message: 'Impossible de charger l\'historique des paiements',
            duration: 5000
        });
        console.error('Error loading payments:', err);
    } finally {
        loadingPayments.value = false;
    }
};

// Load dashboard statistics
const loadDashboardStats = async () => {
    try {
        const data = await apiFetch('/api/reservations/dashboard-stats/');
        stats.value = data;
    } catch (err) {
        console.error('Error loading stats:', err);
        push.error({
            message: 'Impossible de charger les statistiques',
            duration: 5000
        });
    }
};

// Load occupancy statistics
const loadOccupancyStats = async () => {
    loadingOccupancy.value = true;
    try {
        const data = await apiFetch('/api/rooms/occupancy-stats/');
        occupancyStats.value = data;
    } catch (err) {
        console.error('Error loading occupancy:', err);
        push.error({
            message: 'Impossible de charger les données d\'occupation',
            duration: 5000
        });
    } finally {
        loadingOccupancy.value = false;
    }
};

// Helper functions
const formatPrice = (price) => {
    return formatCurrency(price);
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

// Lifecycle
onMounted(async () => {
    await Promise.all([
        loadDashboardStats(),
        loadOccupancyStats(),
        loadPaymentsHistory(),
        loadCompanyInfo()
    ]);
});
</script>

<style>

</style>