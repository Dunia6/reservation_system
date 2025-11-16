<template>
    <div class="bg-linear-to-br from-gray-50 to-gray-100 min-h-screen flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden border border-gray-200">
        <!-- Header -->
        <div class="p-10 text-center bg-linear-to-b from-white to-gray-50">
            <div class="mx-auto mb-6 flex items-center justify-center">
                <img :src="logo" alt="Logo Hôtel" class="h-20 w-auto object-contain">
            </div>
            <p class="text-gray-500 mt-2 text-sm font-light">Système de réservation</p>
        </div>

        <!-- Login Form -->
        <div class="px-10 py-8">
            <h2 class="text-lg font-medium text-gray-900 mb-8">Connexion</h2>

            <form method="POST" @submit.prevent="handleLogin" class="space-y-6">
                <!-- Username -->
                <div>
                    <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
                        Nom d'utilisateur
                    </label>
                    <input type="text" id="username" v-model="username" required
                        class="block w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900 transition text-gray-900"
                        placeholder="Entrez votre nom d'utilisateur">
                </div>

                <!-- Password -->
                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
                        Mot de passe
                    </label>
                    <input type="password" id="password" v-model="password" required
                        class="block w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-gray-900 transition text-gray-900"
                        placeholder="Entrez votre mot de passe">
                </div>

                <!-- Submit Button -->
                <button type="submit"
                    class="w-full bg-gray-900 text-white py-3.5 px-4 rounded-lg font-medium hover:bg-black focus:outline-none focus:ring-2 focus:ring-gray-900 focus:ring-offset-2 transition duration-200 mt-8">
                    Se connecter
                </button>
            </form>
        </div>

        <!-- Footer -->
        <div class="bg-gray-50 px-10 py-5 text-center border-t border-gray-200">
            <p class="text-xs text-gray-600 font-light">
                © <span id="year"></span> Made with ❤️ by <strong class="font-semibold text-gray-800">Jephté Dunia (GMT)</strong>. Tous droits réservés.
            </p>
        </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import router from '@/router';
import { useAuthStore } from '@/stores/authStore';
import logo from '@/assets/images/logo.png';

const authStore = useAuthStore();
const username = ref('');
const password = ref('');

const handleLogin = async () => {
    try {
        const response = await authStore.login({ 
            username: username.value, 
            password: password.value 
        });

        // Vérifier si la réponse existe
        if (!response) {
            console.error("Login error: No response received");
            alert("Erreur de connexion. Veuillez réessayer.");
            return;
        }

        if (response.success) {
            // Redirection réussie vers la page d'accueil
            await router.push('/');
        } else {
            // Afficher l'erreur
            console.error("Login error:", response.error);
            alert(response.error || "Erreur de connexion");
        }
    } catch (error) {
        console.error("Login failed:", error);
        alert("Erreur de connexion. Veuillez réessayer.");
    }
};


</script>

<style>

</style>