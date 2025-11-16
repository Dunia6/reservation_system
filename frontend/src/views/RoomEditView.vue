<template>
    <div class="container mx-auto px-6 py-8">
        <!-- Page Title -->
        <div class="mb-6">
            <RouterLink to="/hotel-config" class="text-blue-600 hover:text-blue-800 text-sm font-medium mb-2 inline-block">
                ← Retour
            </RouterLink>
            <h1 class="text-2xl font-bold text-gray-900">
                {{ isEditMode ? 'Modifier la Chambre' : 'Ajouter une Chambre' }}
            </h1>
        </div>
        <!-- Form -->
        <div class="bg-white rounded-xl shadow-md border border-gray-200 p-8">
            <form @submit.prevent="handleSubmit">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- Room Number -->
                    <div>
                        <label for="number" class="block text-sm font-medium text-gray-700 mb-2">
                            Numéro de Chambre <span class="text-red-500">*</span>
                        </label>
                        <input
                            type="text"
                            id="number"
                            v-model="formData.number"
                            required
                            :disabled="isEditMode"
                            class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            :class="{ 'bg-gray-100 cursor-not-allowed': isEditMode }"
                            placeholder="Ex: 101"
                        />
                        <p v-if="isEditMode" class="mt-1 text-xs text-gray-500">
                            Le numéro de chambre ne peut pas être modifié
                        </p>
                    </div>

                    <!-- Floor -->
                    <div>
                        <label for="floor" class="block text-sm font-medium text-gray-700 mb-2">
                            Niveau <span class="text-red-500">*</span>
                        </label>
                        <select
                            id="floor"
                            v-model="formData.floor_id"
                            required
                            class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="">Sélectionner un niveau</option>
                            <option v-for="floor in floors" :key="floor.id" :value="floor.id">
                                Niveau {{ floor.number }}
                            </option>
                        </select>
                    </div>

                    <!-- Room Type -->
                    <div>
                        <label for="type" class="block text-sm font-medium text-gray-700 mb-2">
                            Catégorie <span class="text-red-500">*</span>
                        </label>
                        <select
                            id="type"
                            v-model="formData.type_id"
                            required
                            class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="">Sélectionner une catégorie</option>
                            <option v-for="type in roomTypes" :key="type.id" :value="type.id">
                                {{ type.name }} - {{ formatCurrency(type.price_per_night) }}/nuit
                            </option>
                        </select>
                    </div>

                    <!-- Status -->
                    <div>
                        <label for="status" class="block text-sm font-medium text-gray-700 mb-2">
                            Statut <span class="text-red-500">*</span>
                        </label>
                        <select
                            id="status"
                            v-model="formData.status"
                            required
                            class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="available">Disponible</option>
                            <option value="occupied">Occupé</option>
                            <option value="maintenance">En Maintenance</option>
                        </select>
                    </div>

                    <!-- Is Available -->
                    <div class="md:col-span-2">
                        <label class="flex items-center space-x-3 cursor-pointer">
                            <input
                                type="checkbox"
                                v-model="formData.is_available"
                                class="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                            />
                            <span class="text-sm font-medium text-gray-700">
                                Chambre disponible pour réservation
                            </span>
                        </label>
                        <p class="mt-1 text-xs text-gray-500 ml-8">
                            Décochez cette option pour rendre la chambre temporairement indisponible
                        </p>
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
                        :disabled="loading"
                        class="px-6 py-2.5 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <span v-if="loading" class="flex items-center">
                            <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Traitement...
                        </span>
                        <span v-else>
                            {{ isEditMode ? 'Mettre à jour' : 'Ajouter' }}
                        </span>
                    </button>
                </div>
            </form>
        </div>

        <!-- Room Preview (Edit Mode Only) -->
        <div v-if="isEditMode && currentRoom" class="bg-white rounded-xl shadow-md border border-gray-200 p-6 mt-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Informations Actuelles</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-xs text-gray-600 mb-1">Numéro de Chambre</p>
                    <p class="text-sm font-semibold text-gray-900">{{ currentRoom.number }}</p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-xs text-gray-600 mb-1">Niveau</p>
                    <p class="text-sm font-semibold text-gray-900">Niveau {{ currentRoom.floor?.number }}</p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-xs text-gray-600 mb-1">Catégorie</p>
                    <p class="text-sm font-semibold text-gray-900">{{ currentRoom.type?.name }}</p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-xs text-gray-600 mb-1">Statut</p>
                    <span class="inline-block px-3 py-1 rounded-full text-xs font-semibold" :class="getStatusClass(currentRoom.status)">
                        {{ getStatusLabel(currentRoom.status) }}
                    </span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter, RouterLink } from 'vue-router';
import { useRoomStore } from '@/stores/roomStore';
import { useAuthStore } from '@/stores/authStore';
import { storeToRefs } from 'pinia';
import { apiFetch } from '@/services/apiService';
import { push } from 'notivue';
import { useCurrency } from '@/composables/useCurrency';

const route = useRoute();
const router = useRouter();
const roomStore = useRoomStore();
const authStore = useAuthStore();

const { currentRoom, loading: storeLoading } = storeToRefs(roomStore);
const { formatCurrency, loadCompanyInfo } = useCurrency();

// State
const loading = ref(false);
const error = ref(null);
const floors = ref([]);
const roomTypes = ref([]);

const formData = ref({
    number: '',
    floor_id: '',
    type_id: '',
    status: 'available',
    is_available: true
});

// Computed
const isEditMode = computed(() => !!route.params.id);

const initials = computed(() => {
    const user = authStore.user;
    if (!user?.username) return 'U';
    return user.username.substring(0, 2).toUpperCase();
});

// Helper functions
const getStatusClass = (status) => {
    const classes = {
        'available': 'bg-green-100 text-green-800',
        'occupied': 'bg-red-100 text-red-800',
        'maintenance': 'bg-amber-100 text-amber-800'
    };
    return classes[status] || 'bg-gray-100 text-gray-800';
};

const getStatusLabel = (status) => {
    const labels = {
        'available': 'Disponible',
        'occupied': 'Occupé',
        'maintenance': 'Maintenance'
    };
    return labels[status] || status;
};

// Load floors and room types
const loadData = async () => {
    try {
        const [floorsData, typesData] = await Promise.all([
            apiFetch('/api/floors/'),
            apiFetch('/api/room-types/')
        ]);
        floors.value = floorsData;
        roomTypes.value = typesData;
    } catch (e) {
        push.error({
            message: 'Erreur lors du chargement des données: ' + e.message,
            duration: 5000
        });
    }
};

// Load room data for edit mode
const loadRoomData = async () => {
    if (!isEditMode.value) return;
    
    try {
        await roomStore.getRoomById(route.params.id);
        if (currentRoom.value) {
            formData.value = {
                number: currentRoom.value.number,
                floor_id: currentRoom.value.floor?.id || '',
                type_id: currentRoom.value.type?.id || '',
                status: currentRoom.value.status || 'available',
                is_available: currentRoom.value.is_available
            };
        }
    } catch (e) {
        push.error({
            message: 'Erreur lors du chargement de la chambre: ' + e.message,
            duration: 5000
        });
    }
};

// Handle form submission
const handleSubmit = async () => {
    loading.value = true;
    error.value = null;

    try {
        const payload = {
            number: formData.value.number,
            floor_id: formData.value.floor_id,
            type_id: formData.value.type_id,
            status: formData.value.status,
            is_available: formData.value.is_available
        };

        if (isEditMode.value) {
            // Update existing room
            await apiFetch(`/api/rooms/${route.params.id}/`, {
                method: 'PUT',
                body: JSON.stringify(payload)
            });
            
            push.success({
                message: 'Chambre mise à jour avec succès!',
                duration: 3000
            });
            
            // Reload room data
            await loadRoomData();
            
            // Redirect after 1 second
            setTimeout(() => {
                router.push('/hotel-config');
            }, 1000);
        } else {
            // Create new room
            await apiFetch('/api/rooms/', {
                method: 'POST',
                body: JSON.stringify(payload)
            });
            
            push.success({
                message: 'Chambre créée avec succès!',
                duration: 3000
            });
            
            // Redirect after 1 second
            setTimeout(() => {
                router.push('/hotel-config');
            }, 1000);
        }

        // Refresh rooms list
        await roomStore.fetchRooms();
    } catch (e) {
        push.error({
            message: isEditMode.value 
                ? 'Erreur lors de la mise à jour: ' + e.message
                : 'Erreur lors de la création: ' + e.message,
            duration: 5000
        });
    } finally {
        loading.value = false;
    }
};

// Lifecycle
onMounted(async () => {
    await Promise.all([
        loadData(),
        loadRoomData(),
        loadCompanyInfo()
    ]);
});
</script>

<style scoped>
/* Custom styles if needed */
</style>
