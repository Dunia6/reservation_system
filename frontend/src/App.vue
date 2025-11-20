<script setup>
import { onMounted, computed } from 'vue';
import { useAuthStore } from './stores/authStore';
import { usePermissions } from '@/composables/usePermissions';
import { useRouter, useRoute } from 'vue-router';
import { storeToRefs } from 'pinia';
import { Notivue, Notification } from 'notivue';
import logo from '@/assets/images/logo.png';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();
const { isAuthenticated } = storeToRefs(authStore);
const { canAccessDashboard, canManageConfig } = usePermissions();
const { user } = storeToRefs(authStore);

const showHeader = computed(() => {
    // Afficher le header sur toutes les pages sauf la page de login
    return route.path !== '/login' && isAuthenticated.value &&  route.name !== 'invoice';
});

const logout = async () => {
    await authStore.logout();

    router.push('/login');
};

onMounted(() => {
    authStore.refreshAccessToken();
});


</script>

<template>
    <Notivue v-slot="item">
        <Notification :item="item" />
    </Notivue>
    
    <!-- Header -->
    <header v-if="showHeader" class="bg-white border-b border-gray-200">
        <div class="container mx-auto px-6 py-5">
            <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4">
                    <div class="h-12">
                        <img :src="logo" alt="Logo Hôtel" class="h-full w-auto object-contain">
                    </div>
                    <div>
                        <h1 class="text-xl font-semibold text-gray-900">Gestion Hôtel</h1>
                        <p class="text-sm text-gray-500">Chambres disponibles</p>
                    </div>
                </div>
                <div class="flex items-center space-x-4">
                    <span class="text-sm text-gray-700 font-medium">
                        {{ user?.username || 'Utilisateur' }}
                    </span>
                    <div class="w-10 h-10 bg-gray-900 rounded-full flex items-center justify-center text-white font-medium text-sm">
                        {{ user?.username?.substring(0, 2).toUpperCase() || 'U' }}
                    </div>
                    <button @click="logout" class="text-gray-600 hover:text-gray-900 transition">
                        <span class="text-sm font-medium">Déconnexion</span>
                    </button>
                </div>
            </div>
        </div>
    </header>

    <!-- Action Menu -->
    <div v-if="showHeader" class="bg-gray-900 border-b border-gray-800">
        <div class="container mx-auto px-6 py-4">
            <div class="flex flex-wrap gap-2">
                <router-link to="/" class="bg-white text-gray-900 px-5 py-2.5 rounded-lg font-medium hover:bg-gray-100 transition">
                    Chambres
                </router-link>
                <router-link to="/reservation" class="bg-white text-gray-900 px-5 py-2.5 rounded-lg font-medium hover:bg-gray-100 transition">
                    Réservation
                </router-link>
                <router-link to="/reservations" class="bg-white text-gray-900 px-5 py-2.5 rounded-lg font-medium hover:bg-gray-100 transition">
                    Liste des réservations
                </router-link>
                <router-link to="/room-change" class="bg-white text-gray-900 px-5 py-2.5 rounded-lg font-medium hover:bg-gray-100 transition">
                    Échange des chambres
                </router-link>
                <router-link 
                    v-permission="'canAccessDashboard'"
                    to="/dashboard" 
                    class="bg-white text-gray-900 px-5 py-2.5 rounded-lg font-medium hover:bg-gray-100 transition"
                >
                    Dashboard
                </router-link>
                <router-link 
                    v-permission="'canManageConfig'"
                    to="/hotel-config" 
                    class="bg-white text-gray-900 px-5 py-2.5 rounded-lg font-medium hover:bg-gray-100 transition"
                >
                    Configuration
                </router-link>
            </div>
        </div>
    </div>
    
    <router-view></router-view>
</template>

<style scoped>

</style>