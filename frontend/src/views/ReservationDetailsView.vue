<template>
    <!-- Header -->
    <header class="bg-white border-b border-gray-200">
        <div class="container mx-auto px-6 py-5">
            <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4">
                    <RouterLink to="/reservations" class="text-gray-600 hover:text-gray-900 transition">
                        <span class="text-sm font-medium">← Retour</span>
                    </RouterLink>
                    <h1 class="text-xl font-semibold text-gray-900">
                        Détail de la Réservation {{ reservation ? `#${reservation.id}` : '' }}
                    </h1>
                </div>
                <div class="flex items-center space-x-4">
                    <!-- Bouton d'annulation -->
                    <button
                        v-if="reservation && canCancelReservation(reservation.status) && hasPermissionToCancel"
                        @click="cancelReservation"
                        class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition flex items-center gap-2 font-medium"
                        :disabled="cancelling"
                    >
                        <svg v-if="!cancelling" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                        <div v-else class="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                        {{ cancelling ? 'Annulation...' : 'Annuler la Réservation' }}
                    </button>
                </div>
            </div>
        </div>
    </header>

    <!-- Loading State -->
    <div v-if="loading" class="container mx-auto px-6 py-20">
        <div class="flex justify-center items-center">
            <div class="text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto mb-4"></div>
                <p class="text-gray-600">Chargement des détails...</p>
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

    <!-- No Data State -->
    <div v-else-if="!reservation && !loading" class="container mx-auto px-6 py-20">
        <div class="bg-yellow-50 border border-yellow-200 rounded-xl p-6 text-center">
            <p class="text-yellow-600 font-medium mb-4">Aucune réservation trouvée</p>
            <RouterLink to="/reservations" class="bg-yellow-600 text-white px-6 py-2 rounded-lg hover:bg-yellow-700 transition inline-block">
                Retour à la liste
            </RouterLink>
        </div>
    </div>

    <!-- Content -->
    <div v-else-if="reservation" class="container mx-auto px-6 py-8">
        <!-- Debug Info (à retirer en production) -->
        <!-- <pre class="bg-gray-100 p-4 rounded mb-4 text-xs overflow-auto">{{ reservation }}</pre> -->
        
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Main Content -->
            <div class="lg:col-span-2 space-y-6">
                <!-- Status Banner -->
                <div :class="getStatusBannerClass(reservation.status)">
                    <div class="flex items-center justify-between">
                        <div>
                            <h2 class="text-xl font-semibold">{{ getStatusLabel(reservation.status) }}</h2>
                            <p class="mt-1 opacity-90">{{ getStatusDescription(reservation.status) }}</p>
                        </div>
                        <div :class="getStatusBadgeClass(reservation.status)">
                            {{ getStatusLabel(reservation.status).toUpperCase() }}
                        </div>
                    </div>
                </div>

                <!-- Cancelled Reservation Info Banner -->
                <div v-if="reservation.status === 'cancelled'" class="bg-red-50 border-l-4 border-red-500 rounded-lg p-4">
                    <div class="flex items-start">
                        <svg class="w-6 h-6 text-red-500 mr-3 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                        </svg>
                        <div class="flex-1">
                            <h4 class="text-red-800 font-bold mb-1">Réservation annulée</h4>
                            <p class="text-red-700 text-sm mb-2">
                                Cette réservation a été annulée. Toutes les chambres ont été libérées et sont à nouveau disponibles.
                            </p>
                            <div class="bg-white border border-red-200 rounded p-3 mt-2">
                                <p class="text-xs text-red-600 font-medium mb-1">📌 Informations conservées :</p>
                                <ul class="text-xs text-red-600 space-y-1">
                                    <li>✓ Montant payé : {{ formatCurrency(reservation.paid_amount) }} (pour remboursement)</li>
                                    <li>✓ Historique complet de la réservation</li>
                                    <li>✓ Informations du client</li>
                                    <li>✓ Chambres réservées : {{ reservation.reservation_rooms.map(r => r.room_number).join(', ') }}</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Client Information -->
                <div class="bg-white rounded-xl border border-gray-200 p-6">
                    <h3 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
                        <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                        </svg>
                        Informations du Client
                    </h3>
                    <div class="grid grid-cols-2 gap-4">
                        <div class="border-b pb-3">
                            <p class="text-sm text-gray-600">Nom complet</p>
                            <p class="font-semibold text-gray-800">{{ reservation.guest.name }}</p>
                        </div>
                        <div class="border-b pb-3">
                            <p class="text-sm text-gray-600">Sexe</p>
                            <p class="font-semibold text-gray-800">{{ getSexLabel(reservation.guest.sex) }}</p>
                        </div>
                        <div class="border-b pb-3">
                            <p class="text-sm text-gray-600">Type pièce d'identité</p>
                            <p class="font-semibold text-gray-800">{{ reservation.guest.type_of_id }}</p>
                        </div>
                        <div class="border-b pb-3">
                            <p class="text-sm text-gray-600">Numéro pièce</p>
                            <p class="font-semibold text-gray-800">{{ reservation.guest.id_number }}</p>
                        </div>
                        <div class="border-b pb-3">
                            <p class="text-sm text-gray-600">Téléphone</p>
                            <p class="font-semibold text-gray-800">{{ reservation.guest.contact_number }}</p>
                        </div>
                        <div v-if="reservation.guest.email" class="border-b pb-3">
                            <p class="text-sm text-gray-600">Email</p>
                            <p class="font-semibold text-gray-800">{{ reservation.guest.email }}</p>
                        </div>
                    </div>
                </div>

                <!-- Rooms Information -->
                <div class="bg-white rounded-lg border border-gray-200 p-6">
                    <h3 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
                        <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
                        </svg>
                        Chambres Réservées ({{ reservation.reservation_rooms?.length || 0 }})
                    </h3>
                    <div class="space-y-3">
                        <div v-for="room in (reservation.reservation_rooms || [])" :key="room.id" 
                             :class="[
                                'p-4 rounded-lg border',
                                isRoomOverdue(room) ? 'bg-red-50 border-red-300' : 'bg-gray-50 border-gray-200'
                             ]">
                            <!-- Alerte de retard -->
                            <div v-if="isRoomOverdue(room)" class="mb-3 bg-red-100 border border-red-400 rounded-lg p-3 flex items-start gap-2">
                                <svg class="w-5 h-5 text-red-600 shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
                                </svg>
                                <div>
                                    <p class="font-semibold text-red-800 text-sm">⚠️ Chambre non libérée !</p>
                                    <p class="text-red-700 text-xs mt-1">
                                        La date de sortie était le {{ formatDate(reservation.check_out_date) }} 
                                        <span v-if="reservation.check_out_time">à {{ reservation.check_out_time }}</span>.
                                        <br>Veuillez libérer cette chambre immédiatement.
                                    </p>
                                </div>
                            </div>

                            <div class="flex justify-between items-start mb-3">
                                <div class="flex items-center gap-2">
                                    <h4 class="font-semibold text-lg text-gray-800">Chambre {{ room.room_number }}</h4>
                                    <span v-if="isRoomOverdue(room)" class="animate-pulse bg-red-500 text-white text-xs px-2 py-1 rounded-full font-bold">
                                        EN RETARD
                                    </span>
                                </div>
                                <button 
                                    v-if="room.room_status !== 'available'"
                                    @click="releaseRoom(room)"
                                    :class="[
                                        'text-white px-3 py-1 rounded text-sm font-medium transition flex items-center gap-1',
                                        isRoomOverdue(room) ? 'bg-red-600 hover:bg-red-700 animate-pulse' : 'bg-orange-500 hover:bg-orange-600'
                                    ]"
                                >
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z"></path>
                                    </svg>
                                    {{ isRoomOverdue(room) ? 'LIBÉRER MAINTENANT' : 'Libérer' }}
                                </button>
                            </div>
                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <p class="text-sm text-gray-600">Type</p>
                                    <p class="font-semibold text-gray-800">{{ room.room_type }}</p>
                                </div>
                                <div>
                                    <p class="text-sm text-gray-600">Prix par jour</p>
                                    <p class="font-semibold text-green-600">{{ formatCurrency(room.price_per_day) }}</p>
                                </div>
                                <div>
                                    <p class="text-sm text-gray-600">Sous-total</p>
                                    <p class="font-semibold text-green-600">{{ formatCurrency(calculateRoomTotal(room.price_per_day)) }}</p>
                                </div>
                                <div>
                                    <p class="text-sm text-gray-600">Statut</p>
                                    <span :class="getRoomStatusBadge(room.room_status)">
                                        {{ room.room_status == 'available' ? 'Disponible' : 'Occupée' }}
                                    </span>
                                </div>
                                <div v-if="room.notes" class="col-span-2">
                                    <p class="text-sm text-gray-600">Notes</p>
                                    <p class="text-gray-800">{{ room.notes }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Reservation Details -->
                <div class="bg-white rounded-lg border border-gray-200 p-6">
                    <h3 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
                        <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                        </svg>
                        Détails de la Réservation
                    </h3>
                    <div class="grid grid-cols-2 gap-4">
                        <div class="border-b pb-3">
                            <p class="text-sm text-gray-600">Nombre de personnes</p>
                            <p class="font-semibold text-gray-800">{{ reservation.people_count }} personne(s)</p>
                        </div>
                        <div class="border-b pb-3">
                            <p class="text-sm text-gray-600">Nombre de clés</p>
                            <p class="font-semibold text-gray-800">{{ reservation.keys_count }} clé(s)</p>
                        </div>
                        <div class="border-b pb-3">
                            <p class="text-sm text-gray-600">Date d'arrivée</p>
                            <p class="font-semibold text-gray-800">{{ formatDateTime(reservation.check_in) }}</p>
                        </div>
                        <div class="border-b pb-3">
                            <p class="text-sm text-gray-600">Nombre de jours</p>
                            <p class="font-semibold text-gray-800">{{ reservation.number_of_days }} jour(s)</p>
                        </div>
                        <div v-if="reservation.check_out_date" class="border-b pb-3">
                            <p class="text-sm text-gray-600">Date de départ</p>
                            <p class="font-semibold text-gray-800">{{ formatDate(reservation.check_out_date) }}</p>
                        </div>
                        <div v-if="reservation.check_out_time" class="border-b pb-3">
                            <p class="text-sm text-gray-600">Heure de départ</p>
                            <p class="font-semibold text-gray-800">{{ reservation.check_out_time }}</p>
                        </div>
                        <div class="border-b pb-3">
                            <p class="text-sm text-gray-600">Créée le</p>
                            <p class="font-semibold text-gray-800">{{ formatDateTime(reservation.created_at) }}</p>
                        </div>
                        <div class="border-b pb-3">
                            <p class="text-sm text-gray-600">Créée par</p>
                            <p class="font-semibold text-gray-800">{{ reservation.created_by_username || 'N/A' }}</p>
                            <p v-if="reservation.created_by_role" class="text-xs text-gray-500 mt-1">{{ reservation.created_by_role }}</p>
                        </div>
                        <div class="border-b pb-3">
                            <p class="text-sm text-gray-600">Dernière mise à jour</p>
                            <p class="font-semibold text-gray-800">{{ formatDateTime(reservation.updated_at) }}</p>
                        </div>
                    </div>
                </div>

                <!-- Payment Information -->
                <div class="bg-white rounded-lg border border-gray-200 p-6">
                    <h3 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
                        <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"></path>
                        </svg>
                        Informations de Paiement
                    </h3>
                    <div class="bg-linear-to-r from-blue-50 to-indigo-100 p-6 rounded-lg border-2 border-blue-200">
                        <div class="space-y-3">
                            <div class="flex justify-between border-b border-blue-200 pb-2">
                                <span class="text-gray-700">Montant total:</span>
                                <span class="font-bold text-green-700 text-xl">{{ formatCurrency(reservation.total_price) }}</span>
                            </div>
                            <div class="flex justify-between border-b border-blue-200 pb-2">
                                <span class="text-gray-700">Montant déposé:</span>
                                <span class="font-semibold text-gray-800">{{ formatCurrency(reservation.paid_amount) }}</span>
                            </div>
                            <div class="flex justify-between border-b border-blue-200 pb-2">
                                <span class="text-gray-700">Statut paiement:</span>
                                <span :class="getPaymentStatusClass(reservation.payment_status)">
                                    {{ getPaymentStatusLabel(reservation.payment_status) }}
                                </span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-700 font-semibold">Reste à payer:</span>
                                <span class="font-bold text-red-600 text-xl">{{ formatCurrency(reservation.remaining_amount) }}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Payment History -->
                <div v-if="reservation.payments && reservation.payments.length > 0" class="bg-white rounded-lg border border-gray-200 p-6">
                    <h3 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
                        <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
                        </svg>
                        Historique des Paiements ({{ reservation.payments.length }})
                    </h3>
                    <div class="overflow-x-auto">
                        <table class="w-full">
                            <thead class="bg-gray-100">
                                <tr>
                                    <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">Date</th>
                                    <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">Méthode</th>
                                    <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">Référence</th>
                                    <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">Créé par</th>
                                    <th class="px-4 py-3 text-right text-sm font-semibold text-gray-700">Montant</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-200">
                                <tr v-for="payment in reservation.payments" :key="payment.id" class="hover:bg-gray-50">
                                    <td class="px-4 py-3 text-sm text-gray-800">{{ formatDateTime(payment.payment_date) }}</td>
                                    <td class="px-4 py-3">
                                        <span class="bg-purple-100 text-purple-800 px-2 py-1 rounded text-xs font-semibold">
                                            {{ payment.payment_method_display }}
                                        </span>
                                    </td>
                                    <td class="px-4 py-3 text-sm text-gray-600">{{ payment.reference_number || '-' }}</td>
                                    <td class="px-4 py-3">
                                        <div class="text-sm font-medium text-gray-800">{{ payment.created_by_username || 'N/A' }}</div>
                                        <div v-if="payment.created_by_role" class="text-xs text-gray-500">{{ payment.created_by_role }}</div>
                                    </td>
                                    <td class="px-4 py-3 text-right font-semibold text-green-700">
                                        {{ formatCurrency(payment.amount) }}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div v-if="reservation.payments.some(p => p.notes)" class="mt-4 space-y-2">
                        <div v-for="payment in reservation.payments.filter(p => p.notes)" :key="`note-${payment.id}`" 
                             class="bg-gray-50 p-3 rounded border-l-4 border-blue-500">
                            <p class="text-xs text-gray-500">{{ formatDateTime(payment.payment_date) }}</p>
                            <p class="text-sm text-gray-700 mt-1">{{ payment.notes }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Sidebar -->
            <div class="space-y-6">
                <!-- Quick Actions -->
                <div class="bg-white rounded-lg border border-gray-200 p-6">
                    <h3 class="text-lg font-bold text-gray-800 mb-4">Actions Rapides</h3>
                    <div class="space-y-3">
                        <RouterLink :to="`/invoices/${reservation.id}`" 
                                    class="block w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-blue-700 transition text-center">
                            <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path>
                            </svg>
                            Voir/Imprimer facture
                        </RouterLink>
                        <RouterLink v-if="reservation.payment_status !== 'paid'" 
                                    :to="`/reservations/${reservation.id}/payment`"
                                    class="block w-full bg-green-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-green-700 transition text-center">
                            <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                            Ajouter un paiement
                        </RouterLink>
                        
                    </div>
                </div>

                <!-- Summary Card -->
                <div class="bg-linear-to-r from-blue-500 to-indigo-600 text-white rounded-lg border border-gray-200 p-6">
                    <h3 class="text-lg font-bold mb-4">Résumé Financier</h3>
                    <div class="space-y-3">
                        <div class="flex justify-between pb-2 border-b border-blue-400">
                            <span>Total chambres:</span>
                            <span class="font-semibold">{{ formatCurrency(reservation.total_price) }}</span>
                        </div>
                        <div class="flex justify-between pb-2 border-b border-blue-400">
                            <span class="font-bold">Total:</span>
                            <span class="font-bold text-xl">{{ formatCurrency(reservation.total_price) }}</span>
                        </div>
                        <div class="flex justify-between pb-2 border-b border-blue-400">
                            <span>Payé:</span>
                            <span class="font-semibold">{{ formatCurrency(reservation.paid_amount) }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="font-bold">À payer:</span>
                            <span class="font-bold text-xl">{{ formatCurrency(reservation.remaining_amount) }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useReservationStore } from '@/stores/reservationStore';
import { useAuthStore } from '@/stores/authStore';
import { usePermissions } from '@/composables/usePermissions';
import { onMounted, computed } from 'vue';
import { storeToRefs } from 'pinia';
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { push } from 'notivue';
import { apiFetch } from '@/services/apiService';
import { useCurrency } from '@/composables/useCurrency';

const router = useRouter();
const route = useRoute();
const reservationStore = useReservationStore();
const authStore = useAuthStore();
const { canCancelReservation: hasPermissionToCancel } = usePermissions();

const { currentReservation: reservation, loading, error } = storeToRefs(reservationStore);
const { formatCurrency, loadCompanyInfo } = useCurrency();

onMounted(async () => {
    const id = route.params.id;
    console.log('Loading reservation with ID:', id);
    await Promise.all([
        reservationStore.getReservationById(id),
        loadCompanyInfo()
    ]);
    console.log('Reservation loaded:', reservation.value);
});

// Computed
const initials = computed(() => {
    if (!authStore.user?.username) return '?';
    const name = authStore.user.username.toUpperCase();
    return name.slice(0, 2);
});

// Helper functions
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

const formatDate = (date) => {
    if (!date) return 'N/A';
    const d = new Date(date);
    return d.toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
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

const getStatusDescription = (status) => {
    const descriptions = {
        'pending': 'Cette réservation est en attente de confirmation',
        'confirmed': 'Cette réservation est confirmée',
        'checked_in': 'Le client est actuellement dans l\'hôtel',
        'checked_out': 'Le client a quitté l\'hôtel',
        'cancelled': 'Cette réservation a été annulée'
    };
    return descriptions[status] || '';
};

const getStatusBannerClass = (status) => {
    const classes = {
        'pending': 'bg-yellow-50 border border-yellow-200 text-yellow-900 rounded-xl p-6',
        'confirmed': 'bg-blue-50 border border-blue-200 text-blue-900 rounded-xl p-6',
        'checked_in': 'bg-green-50 border border-green-200 text-green-900 rounded-xl p-6',
        'checked_out': 'bg-gray-50 border border-gray-200 text-gray-900 rounded-xl p-6',
        'cancelled': 'bg-red-50 border border-red-200 text-red-900 rounded-xl p-6'
    };
    return classes[status] || 'bg-gray-50 border border-gray-200 text-gray-900 rounded-xl p-6';
};

const getStatusBadgeClass = (status) => {
    const classes = {
        'pending': 'bg-yellow-500 text-white px-4 py-2 rounded-lg font-medium',
        'confirmed': 'bg-blue-500 text-white px-4 py-2 rounded-lg font-medium',
        'checked_in': 'bg-green-500 text-white px-4 py-2 rounded-lg font-medium',
        'checked_out': 'bg-gray-500 text-white px-4 py-2 rounded-lg font-medium',
        'cancelled': 'bg-red-500 text-white px-4 py-2 rounded-lg font-medium'
    };
    return classes[status] || 'bg-gray-500 text-white px-4 py-2 rounded-lg font-medium';
};

const getPaymentStatusLabel = (status) => {
    const labels = {
        'unpaid': 'Non payé',
        'partial': 'Paiement partiel',
        'paid': 'Payé'
    };
    return labels[status] || status;
};

const getRoomStatusBadge = (status) => {
    const classes = {
        'occupied': 'px-2 py-1 rounded text-xs font-semibold bg-red-100 text-red-800',
        'available': 'px-2 py-1 rounded text-xs font-semibold bg-green-100 text-green-800',
        'maintenance': 'px-2 py-1 rounded text-xs font-semibold bg-yellow-100 text-yellow-800'
    };
    return classes[status] || 'px-2 py-1 rounded text-xs font-semibold bg-gray-100 text-gray-800';
};

const isRoomOverdue = (room) => {
    console.log('🔍 Vérification chambre:', room.room_number);
    console.log('  - room_status:', room.room_status);
    console.log('  - check_out_date:', reservation.value?.check_out_date);
    console.log('  - check_out_time:', reservation.value?.check_out_time);
    
    // Vérifier si la chambre est toujours occupée
    // Changement: on vérifie aussi si room_status n'existe pas (chambres occupées par défaut)
    const isOccupied = !room.room_status || room.room_status === 'occupied';
    console.log('  - isOccupied:', isOccupied);
    
    if (!isOccupied) {
        console.log('  ❌ Chambre non occupée');
        return false;
    }
    
    // Vérifier si on a une date de sortie
    if (!reservation.value?.check_out_date) {
        console.log('  ❌ Pas de date de sortie');
        return false;
    }
    
    try {
        // Date et heure actuelles
        const now = new Date();
        
        // Construire la date/heure de sortie prévue
        let checkoutDateTime;
        if (reservation.value.check_out_time) {
            // Combiner date et heure
            checkoutDateTime = new Date(`${reservation.value.check_out_date}T${reservation.value.check_out_time}`);
        } else {
            // Si pas d'heure, utiliser minuit (fin de journée = 23:59:59)
            checkoutDateTime = new Date(reservation.value.check_out_date);
            checkoutDateTime.setHours(23, 59, 59);
        }
        
        console.log('  - now:', now);
        console.log('  - checkoutDateTime:', checkoutDateTime);
        console.log('  - now > checkoutDateTime:', now > checkoutDateTime);
        
        // La chambre est en retard si la date actuelle dépasse la date de sortie
        const overdue = now > checkoutDateTime;
        console.log('  ⚠️ Résultat isRoomOverdue:', overdue);
        return overdue;
    } catch (error) {
        console.error('Erreur lors du calcul de retard:', error);
        return false;
    }
};

const releaseRoom = async (room) => {
    if (!confirm(`Êtes-vous sûr de vouloir libérer la chambre ${room.room_number} ?`)) {
        return;
    }
    
    try {
        // Appel à l'API pour libérer la chambre (changer son statut à 'available')
        await apiFetch(`/api/rooms/${room.room_id}/`, {
            method: 'PATCH',
            body: JSON.stringify({
                status: 'available'
            })
        });
        
        // Notification de succès
        push.success({
            title: 'Succès',
            message: `La chambre ${room.room_number} a été libérée avec succès`
        });
        
        // Recharger les détails de la réservation
        await reservationStore.getReservationById(route.params.id);
    } catch (error) {
        console.error('Erreur lors de la libération:', error);
        push.error({
            title: 'Erreur',
            message: error.message || 'Impossible de libérer la chambre'
        });
    }
};

// État pour l'annulation
const cancelling = ref(false);

// Vérifier si une réservation peut être annulée
const canCancelReservation = (status) => {
    return status !== 'cancelled' && status !== 'checked_out';
};

// Annuler la réservation
const cancelReservation = async () => {
    if (!reservation.value) return;
    
    const confirmMessage = `⚠️ ATTENTION : Êtes-vous sûr de vouloir annuler cette réservation ?\n\n` +
        `Réservation #${reservation.value.id}\n` +
        `Client: ${reservation.value.guest.name}\n` +
        `Chambres: ${reservation.value.reservation_rooms.length}\n` +
        `Montant total: ${formatCurrency(reservation.value.total_price)}\n` +
        `Montant payé: ${formatCurrency(reservation.value.paid_amount)}\n\n` +
        `✓ Toutes les chambres seront libérées\n` +
        `✓ La trace de la réservation sera conservée\n` +
        `✓ Le montant payé sera conservé pour remboursement\n\n` +
        `Cette action est irréversible.`;
    
    if (!confirm(confirmMessage)) {
        return;
    }
    
    cancelling.value = true;
    
    try {
        // Appel à l'endpoint DELETE pour annuler la réservation
        const response = await apiFetch(`/api/reservations/${reservation.value.id}/`, {
            method: 'DELETE'
        });
        
        console.log('Réservation annulée:', response);
        
        // Notification de succès avec détails
        push.success({
            title: '✅ Réservation annulée',
            message: `${response.message}\n${response.rooms_released.length} chambre(s) libérée(s): ${response.rooms_released.join(', ')}`,
            duration: 6000
        });
        
        // Rediriger vers la liste des réservations après 2 secondes
        setTimeout(() => {
            router.push('/reservations');
        }, 2000);
        
    } catch (error) {
        console.error('Erreur lors de l\'annulation:', error);
        
        cancelling.value = false;
        
        push.error({
            title: '❌ Erreur d\'annulation',
            message: error.message || 'Impossible d\'annuler la réservation',
            duration: 5000
        });
    }
};



const getPaymentStatusClass = (status) => {
    const classes = {
        'unpaid': 'font-semibold text-red-600',
        'partial': 'font-semibold text-orange-600',
        'paid': 'font-semibold text-green-600'
    };
    return classes[status] || 'font-semibold text-gray-600';
};

</script>

<style>

</style>