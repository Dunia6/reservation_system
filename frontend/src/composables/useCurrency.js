import { ref, computed } from 'vue';
import { apiFetch } from '@/services/apiService';

const companyInfo = ref(null);
const loading = ref(false);

export function useCurrency() {
    // Charger les informations de l'entreprise si pas encore chargées
    const loadCompanyInfo = async () => {
        if (companyInfo.value) return companyInfo.value;
        
        loading.value = true;
        try {
            const data = await apiFetch('/api/company/current/');
            companyInfo.value = data;
            return data;
        } catch (error) {
            console.error('Erreur lors du chargement des informations de l\'entreprise:', error);
            // Par défaut, utiliser CDF
            companyInfo.value = { currency: 'CDF' };
            return companyInfo.value;
        } finally {
            loading.value = false;
        }
    };

    // Obtenir le code de la devise (ex: "CDF", "USD")
    const currencyCode = computed(() => {
        return companyInfo.value?.currency || 'CDF';
    });

    // Obtenir le symbole de la devise
    const currencySymbol = computed(() => {
        const symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'CDF': 'FC',
            'XAF': 'FCFA',
            'ZAR': 'R',
            'NGN': '₦',
            'KES': 'KSh',
            'TZS': 'TSh',
            'UGX': 'USh',
            'RWF': 'FRw',
            'MAD': 'DH',
            'XOF': 'FCFA'
        };
        return symbols[currencyCode.value] || currencyCode.value;
    });

    // Formater un montant avec la devise
    const formatCurrency = (amount, showCode = false) => {
        if (amount === null || amount === undefined) return '-';
        
        const numAmount = parseFloat(amount);
        if (isNaN(numAmount)) return '-';

        // Formater le nombre avec espaces comme séparateurs de milliers
        const formatted = numAmount.toLocaleString('fr-FR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });

        if (showCode) {
            return `${formatted} ${currencyCode.value}`;
        }
        return `${formatted} ${currencySymbol.value}`;
    };

    // Réinitialiser les informations (utile après modification)
    const refreshCompanyInfo = async () => {
        companyInfo.value = null;
        return await loadCompanyInfo();
    };

    return {
        companyInfo,
        loading,
        currencyCode,
        currencySymbol,
        formatCurrency,
        loadCompanyInfo,
        refreshCompanyInfo
    };
}
