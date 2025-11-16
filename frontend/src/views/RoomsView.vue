<script setup>
import { onMounted, ref, computed } from 'vue';
import { useRoomStore } from '@/stores/roomStore';
import { storeToRefs } from 'pinia';

const roomStore = useRoomStore();

const { rooms, floors, loading } = storeToRefs(roomStore);

// Filtres
const selectedFloor = ref('');
const selectedStatus = ref('');

// Chambres filtrées
const filteredRooms = computed(() => {
    let result = rooms.value;

    // Filtrer par niveau
    if (selectedFloor.value) {
        result = result.filter(room => room.floor.number === parseInt(selectedFloor.value));
    }

    // Filtrer par statut
    if (selectedStatus.value === 'free') {
        result = result.filter(room => room.status === 'available');
    } else if (selectedStatus.value === 'occupied') {
        result = result.filter(room => room.status === 'occupied');
    }

    return result;
});

onMounted(() => {
    roomStore.fetchRooms();
    roomStore.fetchRoomTypes();
    roomStore.fetchFloors();
});


</script>

<template>
    <!-- Filters -->
    <div class="container mx-auto px-6 py-8">
        <div class="bg-white rounded-xl border border-gray-200 p-6 mb-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Filtres</h3>
            <div class="flex flex-wrap gap-4 items-end">
                <div class="flex-1 min-w-64">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Niveau</label>
                    <select 
                        v-model="selectedFloor"
                        class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900 text-gray-900"
                    >
                        <option value="">Tous les niveaux</option>
                        <option v-for="floor in floors" :key="floor.id" :value="floor.number">
                            Niveau {{ floor.number }}
                        </option>
                    </select>
                </div>
                <div class="flex-1 min-w-64">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Statut</label>
                    <select 
                        v-model="selectedStatus"
                        class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900 text-gray-900"
                    >
                        <option value="">Tous les statuts</option>
                        <option value="free">Libre</option>
                        <option value="occupied">Occupé</option>
                    </select>
                </div>
            </div>
            <div v-if="selectedFloor || selectedStatus" class="mt-4 text-sm text-gray-600">
                Résultats: {{ filteredRooms.length }} chambre(s)
            </div>
        </div>
    </div>

    <!-- Rooms Grid -->
    <div class="container mx-auto px-6 pb-10">
        <!-- Loading State -->
        <div v-if="loading" class="flex justify-center items-center py-20">
            <div class="text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto mb-4"></div>
                <p class="text-gray-600">Chargement des chambres...</p>
            </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="filteredRooms.length === 0" class="bg-gray-50 border border-gray-200 rounded-xl p-12 text-center">
            <p class="text-gray-600 text-lg mb-2">Aucune chambre trouvée</p>
            <p class="text-gray-500 text-sm">Essayez de modifier les filtres ou ajoutez des chambres</p>
        </div>

        <!-- Rooms Grid -->
        <div v-else class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 xl:grid-cols-6 gap-4">
            <!-- Room Card -->
            <router-link 
                v-for="room in filteredRooms"
                :key="room.id"
                :to="`/rooms/${room.id}`"
                class="bg-white rounded-xl border border-gray-200 hover:border-gray-400 hover:shadow-lg transition-all overflow-hidden"
            >
                <div class="relative">
                    <div class="h-28 bg-linear-to-br from-gray-100 to-gray-200 flex items-center justify-center">
                        <span class="text-4xl font-light text-gray-400">{{ room.number }}</span>
                    </div>
                    <div class="absolute top-2 right-2">
                        <span 
                            :class="[
                                'px-2.5 py-1 rounded-full text-xs font-medium',
                                room.status === 'available' 
                                    ? 'bg-green-500 text-white' 
                                    : room.status === 'occupied'
                                    ? 'bg-red-500 text-white'
                                    : 'bg-amber-500 text-white'
                            ]"
                        >
                            {{ 
                                room.status === 'available' ? 'Libre' : 
                                room.status === 'occupied' ? 'Occupé' : 
                                'Maintenance' 
                            }}
                        </span>
                    </div>
                </div>
                <div class="p-3">
                    <h3 class="text-base font-semibold text-gray-900 mb-2">Chambre {{ room.number }}</h3>
                    <div class="space-y-1 text-xs text-gray-600">
                        <div class="flex justify-between">
                            <span>Niveau {{ room.floor.number }}</span>
                            <span class="font-semibold text-gray-900">{{ room.type.name }}</span>
                        </div>
                        <div class="text-xs text-gray-500 mt-1">
                            {{ room.type.price_per_night }} $ / nuit
                        </div>
                    </div>
                </div>
            </router-link>
        </div>
    </div>
</template>

<style>

</style>