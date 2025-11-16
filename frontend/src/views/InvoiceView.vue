<template>
    <!-- Print button -->
    <div class="container mx-auto px-6 py-4 print:hidden">
        <div class="flex items-center justify-between mb-4">
            <RouterLink :to="`/reservations/${$route.params.id}`" class="text-blue-600 hover:text-blue-800 text-sm font-medium">
                ← Retour
            </RouterLink>
            <button @click="printInvoice" class="bg-gray-900 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-black transition">
                Imprimer
            </button>
        </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="container mx-auto px-6 py-20">
        <div class="flex justify-center items-center">
            <div class="text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto mb-4"></div>
                <p class="text-gray-600">Chargement de la facture...</p>
            </div>
        </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="container mx-auto px-6 py-20">
        <div class="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
            <p class="text-red-600 font-medium mb-4">{{ error }}</p>
            <RouterLink to="/reservations" class="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition inline-block">
                Retour à la liste
            </RouterLink>
        </div>
    </div>

    <!-- Invoice Content -->
    <div v-else-if="reservation" class="container mx-auto px-6 py-8 print:py-0">
        <div class="max-w-4xl mx-auto bg-white rounded-xl border border-gray-200 print:shadow-none print:border-0">
            <!-- Invoice Header -->
            <div class="border-b-2 border-gray-900 p-8 print:p-6">
                <div class="flex justify-between items-start">
                    <div class="flex items-start space-x-4">
                        <!-- Logo -->
                        <div class="shrink-0">
                            <div class="w-20 h-20 bg-gray-100 rounded-lg border-2 border-gray-300 flex items-center justify-center overflow-hidden">
                                <!-- <img 
                                    v-if="companyInfo?.logo" 
                                    :src="companyInfo.logo" 
                                    alt="Logo" 
                                    class="w-full h-full object-contain"
                                /> -->
                                <img  
                                    :src="logo" 
                                    alt="Logo" 
                                    class="w-full h-full object-contain"
                                />
                                <!-- <svg v-else class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                                </svg> -->
                            </div>
                        </div>
                        
                        <!-- Company Info -->
                        <div>
                            <div v-if="companyInfo" class="mb-3">
                                <h2 class="text-2xl font-bold text-gray-900 mb-1">{{ companyInfo.name }}</h2>
                            </div>
                            <div v-else class="mb-3">
                                <h2 class="text-2xl font-bold text-gray-900">Hôtel</h2>
                            </div>
                            <div v-if="companyInfo" class="text-sm text-gray-600 space-y-1">
                                <p>{{ companyInfo.avenue }}, {{ companyInfo.quarter }}</p>
                                <p>{{ companyInfo.commune }}, {{ companyInfo.city }}</p>
                                <p>Tél: {{ companyInfo.phone }}</p>
                                <p v-if="companyInfo.email">Email: {{ companyInfo.email }}</p>
                            </div>
                            <div v-else class="text-sm text-gray-600 space-y-1">
                                <p>Avenue de la Liberté</p>
                                <p>Kinshasa, RDC</p>
                                <p>Tél: +243 900 000 000</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="text-right">
                        <h2 class="text-3xl font-semibold text-gray-900 mb-2">FACTURE</h2>
                        <p class="text-sm text-gray-600">Date: {{ formatDate(reservation.created_at) }}</p>
                        <p class="text-sm text-gray-600">Heure: {{ formatTime(reservation.created_at) }}</p>
                    </div>
                </div>
            </div>

            <!-- Reservation & Client Info -->
            <div class="p-8 print:p-6">
                <div class="grid grid-cols-2 gap-8 mb-8">
                    <!-- Client Information -->
                    <div>
                        <h3 class="text-lg font-bold text-gray-800 mb-3 border-b pb-2">Informations du Client</h3>
                        <div class="space-y-2 text-sm">
                            <div class="flex justify-between">
                                <span class="text-gray-600">Nom complet:</span>
                                <span class="font-semibold text-gray-800">{{ reservation.guest.name }}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600">Sexe:</span>
                                <span class="font-semibold text-gray-800">{{ getSexLabel(reservation.guest.sex) }}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600">Pièce d'identité:</span>
                                <span class="font-semibold text-gray-800">{{ reservation.guest.type_of_id }}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600">N° Pièce:</span>
                                <span class="font-semibold text-gray-800">{{ reservation.guest.id_number }}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600">Téléphone:</span>
                                <span class="font-semibold text-gray-800">{{ reservation.guest.contact_number }}</span>
                            </div>
                            <div v-if="reservation.guest.email" class="flex justify-between">
                                <span class="text-gray-600">Email:</span>
                                <span class="font-semibold text-gray-800">{{ reservation.guest.email }}</span>
                            </div>
                        </div>
                    </div>

                    <!-- Reservation Information -->
                    <div>
                        <h3 class="text-lg font-bold text-gray-800 mb-3 border-b pb-2">Informations de Réservation</h3>
                        <div class="space-y-2 text-sm">
                            <div class="flex justify-between">
                                <span class="text-gray-600">N° Réservation:</span>
                                <span class="font-bold text-blue-600">#{{ reservation.id }}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600">Nombre de personnes:</span>
                                <span class="font-semibold text-gray-800">{{ reservation.people_count }}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600">Nombre de clés:</span>
                                <span class="font-semibold text-gray-800">{{ reservation.keys_count }}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600">Date d'arrivée:</span>
                                <span class="font-semibold text-gray-800">{{ formatDateTime(reservation.check_in) }}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600">Date de départ:</span>
                                <span class="font-semibold text-gray-800">{{ formatDate(reservation.check_out_date) }}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600">Durée:</span>
                                <span class="font-semibold text-gray-800">{{ reservation.number_of_days }} jour(s)</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600">Statut:</span>
                                <span class="font-semibold" :class="getStatusTextClass(reservation.status)">
                                    {{ getStatusLabel(reservation.status) }}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Rooms List -->
                <div class="mb-8">
                    <h3 class="text-lg font-bold text-gray-800 mb-3 border-b pb-2">Chambres Réservées</h3>
                    <table class="w-full text-sm">
                        <thead class="bg-gray-100">
                            <tr>
                                <th class="px-4 py-3 text-left text-gray-700 font-semibold">Chambre</th>
                                <th class="px-4 py-3 text-left text-gray-700 font-semibold">Type</th>
                                <th class="px-4 py-3 text-right text-gray-700 font-semibold">Prix/Jour</th>
                                <th class="px-4 py-3 text-right text-gray-700 font-semibold">Jours</th>
                                <th class="px-4 py-3 text-right text-gray-700 font-semibold">Total</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200">
                            <tr v-for="room in reservation.reservation_rooms" :key="room.id">
                                <td class="px-4 py-3 font-semibold text-gray-800">{{ room.room_number }}</td>
                                <td class="px-4 py-3">
                                    <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-semibold">
                                        {{ room.room_type }}
                                    </span>
                                </td>
                                <td class="px-4 py-3 text-right text-gray-800">{{ formatPrice(room.price_per_day) }}</td>
                                <td class="px-4 py-3 text-right text-gray-800">{{ reservation.number_of_days }}</td>
                                <td class="px-4 py-3 text-right font-semibold text-gray-800">
                                    {{ formatPrice(calculateRoomTotal(room.price_per_day)) }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Payment History -->
                <div v-if="reservation.payments && reservation.payments.length > 0" class="mt-8 print:break-inside-avoid">
                    <h3 class="text-lg font-bold text-gray-800 mb-4 border-b-2 border-gray-300 pb-2">
                        Historique des Paiements
                    </h3>
                    <table class="w-full border-collapse">
                        <thead class="bg-gray-100">
                            <tr>
                                <th class="px-4 py-3 text-left text-gray-700 font-semibold">Date</th>
                                <th class="px-4 py-3 text-left text-gray-700 font-semibold">Méthode</th>
                                <th class="px-4 py-3 text-left text-gray-700 font-semibold">Référence</th>
                                <th class="px-4 py-3 text-left text-gray-700 font-semibold">Créé par</th>
                                <th class="px-4 py-3 text-right text-gray-700 font-semibold">Montant</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200">
                            <tr v-for="payment in reservation.payments" :key="payment.id">
                                <td class="px-4 py-3 text-gray-800">{{ formatDateTime(payment.payment_date) }}</td>
                                <td class="px-4 py-3">
                                    <span class="bg-purple-100 text-purple-800 px-2 py-1 rounded text-xs font-semibold">
                                        {{ payment.payment_method_display }}
                                    </span>
                                </td>
                                <td class="px-4 py-3 text-gray-600 text-sm">{{ payment.reference_number || '-' }}</td>
                                <td class="px-4 py-3">
                                    <div class="text-sm font-medium text-gray-800">{{ payment.created_by_username || 'N/A' }}</div>
                                    <div v-if="payment.created_by_role" class="text-xs text-gray-500">{{ payment.created_by_role }}</div>
                                </td>
                                <td class="px-4 py-3 text-right font-semibold text-green-700">
                                    {{ formatPrice(payment.amount) }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Financial Summary -->
                <div class="border-t-2 border-gray-300 pt-6">
                    <div class="flex justify-end">
                        <div class="w-80">
                            <div class="space-y-3">
                                <div class="flex justify-between text-base border-t pt-3">
                                    <span class="font-bold text-gray-800">MONTANT TOTAL:</span>
                                    <span class="font-bold text-gray-800 text-xl">{{ formatPrice(reservation.total_price) }}</span>
                                </div>
                                <div class="flex justify-between text-sm bg-green-50 p-2 rounded">
                                    <span class="text-green-700">Montant Payé:</span>
                                    <span class="font-semibold text-green-700">{{ formatPrice(reservation.paid_amount) }}</span>
                                </div>
                                <div class="flex justify-between text-base bg-red-50 p-2 rounded">
                                    <span class="font-bold text-red-700">RESTE À PAYER:</span>
                                    <span class="font-bold text-red-700 text-xl">{{ formatPrice(reservation.remaining_amount) }}</span>
                                </div>
                                <div class="flex justify-between text-sm bg-blue-50 p-2 rounded">
                                    <span class="text-blue-700">Statut de paiement:</span>
                                    <span class="font-semibold" :class="getPaymentStatusTextClass(reservation.payment_status)">
                                        {{ getPaymentStatusLabel(reservation.payment_status) }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Footer -->
            <div class="bg-gray-50 p-6 border-t print:break-inside-avoid">
                <div class="text-center text-sm text-gray-600">
                    <p class="mb-2">Merci pour votre confiance !</p>
                    <p class="text-xs">Cette facture est générée électroniquement et ne nécessite pas de signature.</p>
                    <p class="text-xs mt-4 text-gray-500">Imprimé le: {{ currentDateTime }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useReservationStore } from '@/stores/reservationStore';
import { ref, onMounted, computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useRoute } from 'vue-router';
import { apiFetch } from '@/services/apiService';
import logo from '@/assets/images/logo.png';
import { useCurrency } from '@/composables/useCurrency';

const route = useRoute();
const reservationStore = useReservationStore();

const { currentReservation: reservation, loading, error } = storeToRefs(reservationStore);
const companyInfo = ref(null);
const { formatCurrency, loadCompanyInfo } = useCurrency();

onMounted(async () => {
    const id = route.params.id;
    console.log('Loading reservation for invoice, ID:', id);
    await Promise.all([
        reservationStore.getReservationById(id),
        loadCompanyInfo()
    ]);
});

// Computed
const currentDateTime = computed(() => {
    const now = new Date();
    return now.toLocaleString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
});

// Helper functions
const formatDate = (date) => {
    if (!date) return 'N/A';
    const d = new Date(date);
    return d.toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
};

const formatTime = (datetime) => {
    if (!datetime) return 'N/A';
    const d = new Date(datetime);
    return d.toLocaleTimeString('fr-FR', {
        hour: '2-digit',
        minute: '2-digit'
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

// Use formatCurrency from composable instead of local formatPrice
const formatPrice = (price) => {
    return formatCurrency(price);
};

const calculateRoomTotal = (pricePerDay) => {
    if (!reservation.value) return 0;
    return parseFloat(pricePerDay) * reservation.value.number_of_days;
};

const getSexLabel = (sex) => {
    return sex === 'M' ? 'Masculin' : 'Féminin';
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

const getStatusTextClass = (status) => {
    const classes = {
        'pending': 'text-yellow-700',
        'confirmed': 'text-blue-700',
        'checked_in': 'text-green-700',
        'checked_out': 'text-gray-700',
        'cancelled': 'text-red-700'
    };
    return classes[status] || 'text-gray-700';
};

const getPaymentStatusLabel = (status) => {
    const labels = {
        'unpaid': 'Non payé',
        'partial': 'Paiement partiel',
        'paid': 'Payé'
    };
    return labels[status] || status;
};

const getPaymentStatusTextClass = (status) => {
    const classes = {
        'unpaid': 'text-red-700',
        'partial': 'text-orange-700',
        'paid': 'text-green-700'
    };
    return classes[status] || 'text-gray-700';
};

const printInvoice = () => {
    window.print();
};
</script>

<style scoped>
@media print {
    body {
        background: white;
    }
    .container {
        max-width: 100%;
        margin: 0;
        padding: 0;
    }
    .print\:hidden {
        display: none !important;
    }
    .print\:shadow-none {
        box-shadow: none !important;
    }
    .print\:p-6 {
        padding: 1.5rem !important;
    }
    .print\:py-0 {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    .print\:break-inside-avoid {
        break-inside: avoid;
    }
}
</style>