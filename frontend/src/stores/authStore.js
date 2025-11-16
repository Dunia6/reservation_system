import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { API_BASE_URL } from '@/config/api'

export const useAuthStore = defineStore("auth", () => {
    // State
    const user = ref(null);
    const accessToken = ref(null);
    const isAuthenticated = computed(() => !!user.value && !!accessToken.value);

    // Actions
    const login = async (credentials) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/accounts/users/login/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify(credentials)
            });

            if (response.ok) {
                const data = await response.json();
                user.value = data.user;
                accessToken.value = data.access;
                return { success: true, data };
            } else {
                const errorData = await response.json().catch(() => ({}));
                console.error("Login failed:", response.statusText);
                return { success: false, error: errorData.message || response.statusText };
            }
        } catch (error) {
            console.error("Login error:", error);
            return { success: false, error: error.message || "Erreur de connexion" };
        }
    };


    const getUser = async () => {
        try {
            console.log("👤 Récupération des infos utilisateur...")
            const response = await fetch(`${API_BASE_URL}/api/accounts/users/me/`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${accessToken.value}`
                },
                credentials: 'include'
            });
            if (response.ok) {
                const data = await response.json();
                
                user.value = data;
                console.log("✅ Utilisateur récupéré:", user.value?.username)
                return { success: true };
            } else {
                console.error("❌ Échec de récupération utilisateur:", response.statusText);
                return { success: false };
            }
        } catch (error) {
            console.error("❌ Erreur lors de la récupération utilisateur:", error);
            return { success: false };
        }
    };


    const refreshAccessToken = async () => {
        try {
            console.log("🔄 Tentative de refresh du token...")
            const response = await fetch(`${API_BASE_URL}/api/accounts/users/refresh/`, {
                method: 'POST',
                credentials: 'include'
            });

            
            if (response.ok) {
                const data = await response.json();
                accessToken.value = data.access;
                
                
                await getUser();
                console.log("✅ Token refreshé avec succès, utilisateur:", user.value?.username)
                return { success: true };
            } else {
                const errorData = await response.json().catch(() => ({}))
                console.error("❌ Échec du refresh:", response.status, errorData)
                return { success: false };
            }
        } catch (error) {
            console.error("❌ Erreur lors du refresh:", error);
            return { success: false };
        }
    };

    
    const initializeSession = async () => {
        try {
            console.log("🚀 Initialisation de la session...")
            
            const result = await refreshAccessToken();
            if (result.success) {
                console.log("✅ Session initialisée avec succès")
            } else {
                console.log("⚠️ Impossible d'initialiser la session (pas de refresh token valide)")
            }
            return result.success;
        } catch (error) {
            console.error("❌ Erreur lors de l'initialisation de la session:", error);
            return false;
        }
    };

    const logout = async () => {
        try {
            await fetch(`${API_BASE_URL}/api/accounts/users/logout/`, {
                method: 'POST',
                credentials: 'include'
            });
        } catch (error) {
            console.error("Error during logout:", error);
        } finally {
            user.value = null;
            accessToken.value = null;
        }
    };



    return {
        user,
        accessToken,
        isAuthenticated,
        login,
        logout,
        getUser,
        refreshAccessToken,
        initializeSession,
    };
});