<template>
    <!-- Loading State -->
    <div v-if="loading" class="container mx-auto px-6 py-20">
        <div class="flex justify-center items-center">
            <div class="text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto mb-4"></div>
                <p class="text-gray-600">Chargement...</p>
            </div>
        </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="container mx-auto px-6 py-20">
        <div class="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
            <p class="text-red-600 font-medium mb-4">{{ error }}</p>
            <RouterLink :to="`/reservations/${$route.params.id}`" class="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition inline-block">
                Retour aux détails
            </RouterLink>
        </div>
    </div>

    <!-- Payment Form -->
    <div v-else-if="reservation" class="container mx-auto px-6 py-8">
        <div class="max-w-2xl mx-auto">
            <!-- Reservation Summary -->
            <div class="bg-white rounded-xl border border-gray-200 p-6 mb-6">
                <h2 class="text-lg font-bold text-gray-800 mb-4">Résumé de la Réservation</h2>
                <div class="grid grid-cols-2 gap-4 text-sm">
                    <div class="flex justify-between">
                        <span class="text-gray-600">N° Réservation:</span>
                        <span class="font-bold text-blue-600">#{{ reservation.id }}</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600">Client:</span>
                        <span class="font-semibold text-gray-800">{{ reservation.guest.name }}</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600">Montant Total:</span>
                        <span class="font-bold text-gray-800">{{ formatPrice(reservation.total_price) }}</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600">Déjà Payé:</span>
                        <span class="font-semibold text-green-600">{{ formatPrice(reservation.paid_amount) }}</span>
                    </div>
                    <div class="col-span-2 pt-2 border-t">
                        <div class="flex justify-between">
                            <span class="text-gray-700 font-bold">Reste à Payer:</span>
                            <span class="font-bold text-red-600 text-xl">{{ formatPrice(reservation.remaining_amount) }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Payment Form -->
            <div class="bg-white rounded-xl border border-gray-200 p-6">
                <h2 class="text-lg font-bold text-gray-800 mb-2">Compléter le Paiement</h2>
                <p class="text-sm text-gray-600 mb-6">
                    Ajoutez un paiement pour compléter le montant restant de cette réservation.
                </p>
                
                <form @submit.prevent="submitPayment" class="space-y-6">
                    <!-- Payment Amount -->
                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-2">
                            Montant du Paiement <span class="text-red-500">*</span>
                        </label>
                        <div class="relative">
                            <input 
                                v-model.number="paymentForm.amount"
                                type="number"
                                step="0.01"
                                min="0"
                                :max="reservation.remaining_amount"
                                required
                                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                                placeholder="Entrez le montant"
                            >
                        </div>
                        <p class="text-xs text-gray-500 mt-1">Maximum: {{ formatPrice(reservation.remaining_amount) }}</p>
                    </div>

                    <!-- Payment Method -->
                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-2">
                            Mode de Paiement <span class="text-red-500">*</span>
                        </label>
                        <select 
                            v-model="paymentForm.payment_method"
                            required
                            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                        >
                            <option value="">Sélectionnez un mode de paiement</option>
                            <option value="cash">Espèces</option>
                            <option value="mobile_money">Mobile Money</option>
                            <option value="bank_transfer">Virement Bancaire</option>
                            <option value="credit_card">Carte de Crédit</option>
                            <option value="check">Chèque</option>
                        </select>
                    </div>

                    <!-- Payment Date -->
                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-2">
                            Date du Paiement <span class="text-red-500">*</span>
                        </label>
                        <input 
                            v-model="paymentForm.payment_date"
                            type="datetime-local"
                            required
                            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                        >
                    </div>

                    <!-- Reference Number -->
                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-2">
                            Numéro de Référence
                        </label>
                        <input 
                            v-model="paymentForm.reference_number"
                            type="text"
                            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                            placeholder="Ex: TXN123456 (optionnel)"
                        >
                        <p class="text-xs text-gray-500 mt-1">Pour Mobile Money, virement bancaire, etc.</p>
                    </div>

                    <!-- Notes -->
                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-2">
                            Notes
                        </label>
                        <textarea 
                            v-model="paymentForm.notes"
                            rows="3"
                            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                            placeholder="Informations supplémentaires sur le paiement (optionnel)"
                        ></textarea>
                    </div>

                    <!-- Payment Status Preview -->
                    <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                        <h3 class="text-sm font-semibold text-blue-800 mb-2">Après ce paiement:</h3>
                        <div class="space-y-1 text-sm">
                            <div class="flex justify-between">
                                <span class="text-blue-700">Total Payé:</span>
                                <span class="font-semibold text-blue-800">
                                    {{ formatPrice(parseFloat(reservation.paid_amount) + (paymentForm.amount || 0)) }}
                                </span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-blue-700">Reste à Payer:</span>
                                <span class="font-semibold text-blue-800">
                                    {{ formatPrice(parseFloat(reservation.remaining_amount) - (paymentForm.amount || 0)) }}
                                </span>
                            </div>
                            <div class="flex justify-between pt-2 border-t border-blue-300">
                                <span class="text-blue-700 font-bold">Nouveau Statut:</span>
                                <span class="font-bold" :class="getNewPaymentStatusClass()">
                                    {{ getNewPaymentStatus() }}
                                </span>
                            </div>
                        </div>
                    </div>

                    <!-- Error Message -->
                    <div v-if="submitError" class="bg-red-50 border border-red-200 rounded-lg p-4">
                        <p class="text-red-600 text-sm">{{ submitError }}</p>
                    </div>

                    <!-- Submit Buttons -->
                    <div class="flex space-x-4 pt-4">
                        <button 
                            type="submit"
                            :disabled="submitting || !isFormValid"
                            class="flex-1 bg-green-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-green-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed"
                        >
                            <span v-if="submitting">Enregistrement...</span>
                            <span v-else>Enregistrer le Paiement</span>
                        </button>
                        <RouterLink 
                            :to="`/reservations/${$route.params.id}`"
                            class="flex-1 bg-gray-200 text-gray-700 py-3 px-6 rounded-lg font-semibold hover:bg-gray-300 transition text-center"
                        >
                            Annuler
                        </RouterLink>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useReservationStore } from '@/stores/reservationStore';
import { useAuthStore } from '@/stores/authStore';
import { onMounted, ref, computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useRoute, useRouter } from 'vue-router';
import { useCurrency } from '@/composables/useCurrency';
import { apiFetch } from '@/services/apiService';
import { push } from 'notivue';

const route = useRoute();
const router = useRouter();
const reservationStore = useReservationStore();
const authStore = useAuthStore();

const { currentReservation: reservation, loading } = storeToRefs(reservationStore);
const submitting = ref(false);
const submitError = ref(null);

const { formatCurrency, loadCompanyInfo } = useCurrency();

// Payment Form
const paymentForm = ref({
    amount: null,
    payment_method: '',
    payment_date: new Date().toISOString().slice(0, 16), // Format YYYY-MM-DDTHH:MM
    reference_number: '',
    notes: ''
});

onMounted(async () => {
    try {
        const id = route.params.id;
        await Promise.all([
            reservationStore.getReservationById(id),
            loadCompanyInfo()
        ]);
        
        // Set default amount to remaining amount
        if (reservation.value) {
            paymentForm.value.amount = parseFloat(reservation.value.remaining_amount);
        }
    } catch (err) {
        push.error({
            message: err.message || "Erreur lors du chargement de la réservation",
            duration: 5000
        });
    }
});

// Computed
const initials = computed(() => {
    if (!authStore.user?.username) return '?';
    const name = authStore.user.username.toUpperCase();
    return name.slice(0, 2);
});

const isFormValid = computed(() => {
    return paymentForm.value.amount > 0 && 
           paymentForm.value.amount <= parseFloat(reservation.value?.remaining_amount || 0) &&
           paymentForm.value.payment_method !== '' &&
           paymentForm.value.payment_date !== '';
});

// Helper functions
const formatPrice = (price) => {
    return formatCurrency(price);
};

const getNewPaymentStatus = () => {
    if (!reservation.value || !paymentForm.value.amount) return 'Non payé';
    
    const newPaidAmount = parseFloat(reservation.value.paid_amount) + parseFloat(paymentForm.value.amount);
    const totalPrice = parseFloat(reservation.value.total_price);
    
    if (newPaidAmount >= totalPrice) {
        return 'Payé';
    } else if (newPaidAmount > 0) {
        return 'Paiement partiel';
    } else {
        return 'Non payé';
    }
};

const getNewPaymentStatusClass = () => {
    const status = getNewPaymentStatus();
    if (status === 'Payé') return 'text-green-700';
    if (status === 'Paiement partiel') return 'text-orange-700';
    return 'text-red-700';
};

const submitPayment = async () => {
    if (!isFormValid.value) return;
    
    submitting.value = true;
    
    try {
        const id = route.params.id;
        
        // Prepare payment data
        const paymentData = {
            amount: parseFloat(paymentForm.value.amount),
            payment_method: paymentForm.value.payment_method,
            payment_date: paymentForm.value.payment_date,
            reference_number: paymentForm.value.reference_number || '',
            notes: paymentForm.value.notes || ''
        };
        
        console.log('📤 Envoi du paiement:', paymentData);
        
        // Send payment to backend
        const response = await apiFetch(`/api/reservations/${id}/add_payment/`, {
            method: 'POST',
            body: JSON.stringify(paymentData)
        });
        
        console.log('✅ Paiement enregistré:', response);
        
        // Refresh reservation data in store before redirecting
        if (response.reservation) {
            await reservationStore.getReservationById(id);
        }
        
        push.success({
            message: 'Paiement enregistré avec succès!',
            duration: 3000
        });
        
        // Redirect to reservation details
        router.push(`/reservations/${id}`);
        
    } catch (err) {
        console.error('❌ Erreur lors de l\'ajout du paiement:', err);
        push.error({
            message: err.message || "Erreur lors de l'enregistrement du paiement",
            duration: 5000
        });
        
        // Scroll to top to show error
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } finally {
        submitting.value = false;
    }
};
</script>

<style scoped>
/* Additional styles if needed */
</style>
