<template>
    <div class="container mx-auto px-6 py-8">
        <!-- Page Title -->
        <div class="mb-6">
            <RouterLink to="/hotel-config" class="text-blue-600 hover:text-blue-800 text-sm font-medium mb-2 inline-block">
                ← Retour
            </RouterLink>
            <h1 class="text-2xl font-bold text-gray-900">Informations de l'Entreprise</h1>
        </div>
        <div class="max-w-4xl mx-auto">
            <!-- Loading State -->
            <div v-if="loading" class="bg-white rounded-xl shadow-md border border-gray-200 p-8">
                <div class="flex justify-center items-center py-12">
                    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
                    <span class="ml-3 text-gray-600">Chargement...</span>
                </div>
            </div>

            <!-- Form -->
            <div v-else class="bg-white rounded-xl shadow-md border border-gray-200 p-8">
                <form @submit.prevent="handleSubmit">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <!-- Company Name -->
                        <div class="md:col-span-2">
                            <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
                                Nom de l'entreprise <span class="text-red-500">*</span>
                            </label>
                            <input
                                type="text"
                                id="name"
                                v-model="formData.name"
                                required
                                class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="Ex: Hôtel Paradis"
                            />
                        </div>

                        <!-- Email -->
                        <div>
                            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
                                Email <span class="text-red-500">*</span>
                            </label>
                            <input
                                type="email"
                                id="email"
                                v-model="formData.email"
                                required
                                class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="contact@hotel.com"
                            />
                        </div>

                        <!-- Phone -->
                        <div>
                            <label for="phone" class="block text-sm font-medium text-gray-700 mb-2">
                                Téléphone <span class="text-red-500">*</span>
                            </label>
                            <input
                                type="tel"
                                id="phone"
                                v-model="formData.phone"
                                required
                                class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="+243 XXX XXX XXX"
                            />
                        </div>

                        <!-- Currency -->
                        <div>
                            <label for="currency" class="block text-sm font-medium text-gray-700 mb-2">
                                Devise <span class="text-red-500">*</span>
                            </label>
                            <select
                                id="currency"
                                v-model="formData.currency"
                                required
                                class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            >
                                <option value="USD">Dollar américain (USD)</option>
                                <option value="EUR">Euro (EUR)</option>
                                <option value="GBP">Livre sterling (GBP)</option>
                                <option value="CDF">Franc congolais (CDF)</option>
                                <option value="XAF">Franc CFA (XAF)</option>
                                <option value="ZAR">Rand sud-africain (ZAR)</option>
                                <option value="NGN">Naira nigérian (NGN)</option>
                                <option value="KES">Shilling kényan (KES)</option>
                                <option value="TZS">Shilling tanzanien (TZS)</option>
                                <option value="UGX">Shilling ougandais (UGX)</option>
                                <option value="RWF">Franc rwandais (RWF)</option>
                                <option value="MAD">Dirham marocain (MAD)</option>
                                <option value="XOF">Franc CFA BCEAO (XOF)</option>
                            </select>
                        </div>

                        <!-- City -->
                        <div>
                            <label for="city" class="block text-sm font-medium text-gray-700 mb-2">
                                Ville <span class="text-red-500">*</span>
                            </label>
                            <input
                                type="text"
                                id="city"
                                v-model="formData.city"
                                required
                                class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="Ex: Kinshasa"
                            />
                        </div>

                        <!-- Commune -->
                        <div>
                            <label for="commune" class="block text-sm font-medium text-gray-700 mb-2">
                                Commune <span class="text-red-500">*</span>
                            </label>
                            <input
                                type="text"
                                id="commune"
                                v-model="formData.commune"
                                required
                                class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="Ex: Gombe"
                            />
                        </div>

                        <!-- Avenue -->
                        <div>
                            <label for="avenue" class="block text-sm font-medium text-gray-700 mb-2">
                                Avenue <span class="text-red-500">*</span>
                            </label>
                            <input
                                type="text"
                                id="avenue"
                                v-model="formData.avenue"
                                required
                                class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="Ex: Av. des Aviateurs"
                            />
                        </div>

                        <!-- Quarter -->
                        <div>
                            <label for="quarter" class="block text-sm font-medium text-gray-700 mb-2">
                                Quartier <span class="text-red-500">*</span>
                            </label>
                            <input
                                type="text"
                                id="quarter"
                                v-model="formData.quarter"
                                required
                                class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="Ex: Centre-ville"
                            />
                        </div>
                    </div>

                    <!-- Actions -->
                    <div class="flex justify-end space-x-4 mt-8 pt-6 border-t border-gray-200">
                        <RouterLink
                            to="/hotel-config"
                            class="px-6 py-2.5 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition"
                        >
                            Annuler
                        </RouterLink>
                        <button
                            type="submit"
                            :disabled="submitting"
                            class="px-6 py-2.5 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            <span v-if="submitting" class="flex items-center">
                                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Enregistrement...
                            </span>
                            <span v-else>
                                Enregistrer
                            </span>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, RouterLink } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import { apiFetch } from '@/services/apiService';
import { push } from 'notivue';

const router = useRouter();
const authStore = useAuthStore();

// State
const loading = ref(false);
const submitting = ref(false);

const formData = ref({
    name: '',
    email: '',
    phone: '',
    city: '',
    commune: '',
    avenue: '',
    quarter: '',
    currency: 'CDF'
});

// Computed
const initials = computed(() => {
    const user = authStore.user;
    if (!user?.username) return 'U';
    return user.username.substring(0, 2).toUpperCase();
});

// Load company information
const loadCompanyInfo = async () => {
    loading.value = true;
    try {
        const data = await apiFetch('/api/company/current/');
        formData.value = {
            name: data.name || '',
            email: data.email || '',
            phone: data.phone || '',
            city: data.city || '',
            commune: data.commune || '',
            avenue: data.avenue || '',
            quarter: data.quarter || '',
            currency: data.currency || 'CDF'
        };
    } catch (error) {
        // If no company info exists, keep empty form
        console.log('No existing company info');
    } finally {
        loading.value = false;
    }
};

// Handle form submission
const handleSubmit = async () => {
    submitting.value = true;
    
    try {
        await apiFetch('/api/company/update_current/', {
            method: 'POST',
            body: JSON.stringify(formData.value)
        });
        
        push.success({
            message: 'Informations de l\'entreprise enregistrées avec succès!',
            duration: 3000
        });
        
        setTimeout(() => {
            router.push('/hotel-config');
        }, 1000);
        
    } catch (error) {
        push.error({
            message: 'Erreur lors de l\'enregistrement: ' + error.message,
            duration: 5000
        });
    } finally {
        submitting.value = false;
    }
};

// Lifecycle
onMounted(() => {
    loadCompanyInfo();
});
</script>

<style scoped>
/* Custom styles if needed */
</style>
