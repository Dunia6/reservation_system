<template>
    <div class="container mx-auto px-6 py-8">
        <!-- Page Title -->
        <div class="mb-6">
            <button @click="$router.back()" class="text-blue-600 hover:text-blue-800 text-sm font-medium mb-2 inline-block">
                ← Retour
            </button>
            <h1 class="text-2xl font-bold text-gray-900">Configuration de l'Hôtel</h1>
        </div>
        <!-- Company Information -->
        <div class="bg-white rounded-xl border border-gray-200 p-6 mb-6">
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-semibold text-gray-900">Informations de l'Entreprise</h3>
                <RouterLink 
                    to="/company-edit" 
                    class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition"
                >
                    Modifier
                </RouterLink>
            </div>
            
            <div v-if="companyLoading" class="flex justify-center py-8">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
            </div>
            
            <div v-else-if="companyInfo" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-xs text-gray-600 mb-1">Nom de l'entreprise</p>
                    <p class="text-sm font-semibold text-gray-900">{{ companyInfo.name }}</p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-xs text-gray-600 mb-1">Email</p>
                    <p class="text-sm font-semibold text-gray-900">{{ companyInfo.email }}</p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-xs text-gray-600 mb-1">Téléphone</p>
                    <p class="text-sm font-semibold text-gray-900">{{ companyInfo.phone }}</p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-xs text-gray-600 mb-1">Devise</p>
                    <p class="text-sm font-semibold text-gray-900">
                        {{ companyInfo.currency_display || companyInfo.currency || 'CDF' }}
                    </p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-xs text-gray-600 mb-1">Ville</p>
                    <p class="text-sm font-semibold text-gray-900">{{ companyInfo.city }}</p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-xs text-gray-600 mb-1">Commune</p>
                    <p class="text-sm font-semibold text-gray-900">{{ companyInfo.commune }}</p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-xs text-gray-600 mb-1">Avenue</p>
                    <p class="text-sm font-semibold text-gray-900">{{ companyInfo.avenue }}</p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-xs text-gray-600 mb-1">Quartier</p>
                    <p class="text-sm font-semibold text-gray-900">{{ companyInfo.quarter }}</p>
                </div>
            </div>
            
            <div v-else class="text-center py-8 text-gray-500">
                <p>Aucune information d'entreprise configurée</p>
                <RouterLink 
                    to="/company-edit" 
                    class="text-blue-600 hover:text-blue-700 text-sm mt-2 inline-block"
                >
                    Configurer maintenant
                </RouterLink>
            </div>
        </div>

        <!-- Action Bar -->
        <div class="bg-white rounded-xl border border-gray-200 p-4 mb-6">
            <div class="flex flex-wrap gap-4 items-center justify-between">
                <RouterLink 
                    to="/rooms/create" 
                    class="bg-gray-900 text-white px-6 py-3 rounded-lg font-medium hover:bg-black transition"
                >
                    Ajouter une chambre
                </RouterLink>
            </div>
        </div>

        <!-- Filters -->
        <div class="bg-white rounded-xl border border-gray-200 p-6 mb-6">
            <h3 class="text-base font-semibold text-gray-900 mb-4">Filtres</h3>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Niveau</label>
                    <select v-model="filters.floor" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        <option value="">Tous les niveaux</option>
                        <option v-for="floor in floors" :key="floor" :value="floor">Niveau {{ floor }}</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Statut</label>
                    <select v-model="filters.status" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900">
                        <option value="">Tous les statuts</option>
                        <option value="available">Disponible</option>
                        <option value="occupied">Occupé</option>
                        <option value="maintenance">Maintenance</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Catégorie</label>
                    <select v-model="filters.type" class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900">
                        <option value="">Toutes les catégories</option>
                        <option v-for="type in roomTypes" :key="type" :value="type">{{ type }}</option>
                    </select>
                </div>
                <div class="flex items-end">
                    <button @click="clearFilters" class="w-full bg-gray-900 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-black transition">
                        Réinitialiser
                    </button>
                </div>
            </div>
        </div>

        <!-- Statistics -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div class="bg-white rounded-xl border border-gray-200 p-5">
                <p class="text-sm text-gray-600">Total Chambres</p>
                <p class="text-3xl font-semibold text-gray-900 mt-1">{{ totalRooms }}</p>
            </div>
            <div class="bg-white rounded-xl border border-gray-200 p-5">
                <p class="text-sm text-gray-600">Chambres Disponibles</p>
                <p class="text-3xl font-semibold text-green-600 mt-1">{{ availableRooms }}</p>
            </div>
            <div class="bg-white rounded-xl border border-gray-200 p-5">
                <p class="text-sm text-gray-600">Chambres Occupées</p>
                <p class="text-3xl font-semibold text-red-600 mt-1">{{ occupiedRooms }}</p>
            </div>
            <div class="bg-white rounded-xl border border-gray-200 p-5">
                <p class="text-sm text-gray-600">En Maintenance</p>
                <p class="text-3xl font-semibold text-amber-600 mt-1">{{ maintenanceRooms }}</p>
            </div>
        </div>

        <!-- Rooms Table -->
        <div class="bg-white rounded-lg shadow-md overflow-hidden">
            <div class="overflow-x-auto">
                <table class="w-full">
                    <thead class="bg-gray-900 text-white">
                        <tr>
                            <th class="px-6 py-4 text-left text-sm font-semibold">Chambre</th>
                            <th class="px-6 py-4 text-left text-sm font-semibold">Niveau</th>
                            <th class="px-6 py-4 text-left text-sm font-semibold">Catégorie</th>
                            <th class="px-6 py-4 text-left text-sm font-semibold">Prix/Jour</th>
                            <th class="px-6 py-4 text-left text-sm font-semibold">Statut</th>
                            <th class="px-6 py-4 text-center text-sm font-semibold">Active</th>
                            <th class="px-6 py-4 text-center text-sm font-semibold">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                        <!-- Loading State -->
                        <tr v-if="loading">
                            <td colspan="7" class="px-6 py-12 text-center">
                                <div class="flex justify-center items-center">
                                    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
                                    <span class="ml-3 text-gray-600">Chargement des chambres...</span>
                                </div>
                            </td>
                        </tr>
                        
                        <!-- No Data State -->
                        <tr v-else-if="filteredRooms.length === 0">
                            <td colspan="7" class="px-6 py-12 text-center text-gray-500">
                                Aucune chambre trouvée
                            </td>
                        </tr>
                        
                        <!-- Room Rows -->
                        <tr v-else v-for="room in filteredRooms" :key="room.id" 
                            class="hover:bg-gray-50 transition"
                            :class="getRowBgClass(room.status)">
                            <td class="px-6 py-4">
                                <div class="flex items-center">
                                    <div class="w-10 h-10 rounded-lg flex items-center justify-center mr-3" 
                                         :class="getIconColorClass(room.status)">
                                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
                                        </svg>
                                    </div>
                                    <div>
                                        <p class="font-semibold text-gray-800">{{ room.number }}</p>
                                        <p class="text-xs text-gray-600">ID: {{ room.id }}</p>
                                    </div>
                                </div>
                            </td>
                            <td class="px-6 py-4 text-sm text-gray-800">Niveau {{ room.floor.number }}</td>
                            <td class="px-6 py-4">
                                <span class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-semibold">
                                    {{ room.type.name }}
                                </span>
                            </td>
                            <td class="px-6 py-4 text-sm font-semibold text-green-600">{{ formatCurrency(room.type.price_per_night) }}</td>
                            <td class="px-6 py-4">
                                <span class="px-3 py-1 rounded-full text-xs font-semibold" :class="getStatusClass(room.status)">
                                    {{ getStatusLabel(room.status) }}
                                </span>
                            </td>
                            <td class="px-6 py-4">
                                <div class="flex justify-center">
                                    <span v-if="room.is_available" class="flex items-center text-green-600">
                                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                                        </svg>
                                    </span>
                                    <span v-else class="flex items-center text-red-600">
                                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
                                        </svg>
                                    </span>
                                </div>
                            </td>
                            <td class="px-6 py-4">
                                <div class="flex justify-center space-x-2">
                                    <RouterLink 
                                        :to="`/rooms/${room.id}/edit`" 
                                        class="bg-blue-600 text-white p-2 rounded hover:bg-blue-700 transition" 
                                        title="Modifier"
                                    >
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                                        </svg>
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
import { useRoomStore } from '@/stores/roomStore';
import { useAuthStore } from '@/stores/authStore';
import { onMounted, computed, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { RouterLink } from 'vue-router';
import { apiFetch } from '@/services/apiService';
import { push } from 'notivue';
import { useCurrency } from '@/composables/useCurrency';

const roomStore = useRoomStore();
const authStore = useAuthStore();
const { rooms, loading } = storeToRefs(roomStore);
const { formatCurrency } = useCurrency();

// Company Information
const companyInfo = ref(null);
const companyLoading = ref(false);

// Filters
const filters = ref({
    floor: '',
    status: '',
    type: ''
});

// Computed: User initials
const initials = computed(() => {
    const user = authStore.user;
    if (!user?.username) return 'U';
    return user.username.substring(0, 2).toUpperCase();
});

// Computed: Filtered rooms
const filteredRooms = computed(() => {
    let result = rooms.value || [];
    
    if (filters.value.floor) {
        result = result.filter(room => room.floor.number === parseInt(filters.value.floor));
    }
    
    if (filters.value.status) {
        result = result.filter(room => room.status === filters.value.status);
    }
    
    if (filters.value.type) {
        result = result.filter(room => room.type.name.toLowerCase() === filters.value.type.toLowerCase());
    }
    
    return result;
});

// Computed: Statistics
const totalRooms = computed(() => filteredRooms.value.length);
const availableRooms = computed(() => filteredRooms.value.filter(r => r.status === 'available').length);
const occupiedRooms = computed(() => filteredRooms.value.filter(r => r.status === 'occupied').length);
const maintenanceRooms = computed(() => filteredRooms.value.filter(r => r.status === 'maintenance').length);

// Computed: Unique floors
const floors = computed(() => {
    const uniqueFloors = [...new Set(rooms.value.map(r => r.floor.number))];
    return uniqueFloors.sort((a, b) => a - b);
});

// Computed: Unique room types
const roomTypes = computed(() => {
    const uniqueTypes = [...new Set(rooms.value.map(r => r.type.name))];
    return uniqueTypes.sort();
});

// Helper: Get status class
const getStatusClass = (status) => {
    const classes = {
        'available': 'bg-green-100 text-green-800',
        'occupied': 'bg-red-100 text-red-800',
        'maintenance': 'bg-amber-100 text-amber-800'
    };
    return classes[status] || 'bg-gray-100 text-gray-800';
};

// Helper: Get status label
const getStatusLabel = (status) => {
    const labels = {
        'available': 'Disponible',
        'occupied': 'Occupé',
        'maintenance': 'Maintenance'
    };
    return labels[status] || status;
};

// Helper: Get icon color class
const getIconColorClass = (status) => {
    const classes = {
        'available': 'bg-green-100 text-green-600',
        'occupied': 'bg-red-100 text-red-600',
        'maintenance': 'bg-amber-100 text-amber-600'
    };
    return classes[status] || 'bg-gray-100 text-gray-600';
};

// Helper: Get row background class
const getRowBgClass = (status) => {
    const classes = {
        'available': '',
        'occupied': 'bg-red-50',
        'maintenance': 'bg-amber-50'
    };
    return classes[status] || '';
};

// Clear filters
const clearFilters = () => {
    filters.value = {
        floor: '',
        status: '',
        type: ''
    };
};

// Load company information
const loadCompanyInfo = async () => {
    companyLoading.value = true;
    try {
        companyInfo.value = await apiFetch('/api/company/current/');
    } catch (error) {
        if (error.message !== 'Aucune information d\'entreprise configurée') {
            push.error({
                message: 'Erreur lors du chargement des informations de l\'entreprise',
                duration: 5000
            });
        }
    } finally {
        companyLoading.value = false;
    }
};

onMounted(() => {
    roomStore.fetchRooms();
    loadCompanyInfo();
});

</script>

<style>

</style>