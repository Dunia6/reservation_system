# Tests Unitaires - Libération et Annulation de Chambres

"""
Tests pour les fonctionnalités de libération et d'annulation de chambres
Fichier: backend/reservation/tests.py
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timedelta

from .models import Reservation, Guest, ReservationRoom, Payment
from rooms.models import Room, RoomType, Floor


class RoomReleaseTestCase(TestCase):
    """Tests pour la libération de chambres"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        # Créer un utilisateur
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Créer le client API
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Créer un type de chambre et un étage
        self.floor = Floor.objects.create(name='1er Étage', floor_number=1)
        self.room_type = RoomType.objects.create(
            name='Standard',
            base_price=50.00,
            capacity=2
        )
        
        # Créer des chambres
        self.room1 = Room.objects.create(
            number='101',
            type=self.room_type,
            floor=self.floor,
            status='available'
        )
        self.room2 = Room.objects.create(
            number='102',
            type=self.room_type,
            floor=self.floor,
            status='available'
        )
        self.room3 = Room.objects.create(
            number='103',
            type=self.room_type,
            floor=self.floor,
            status='available'
        )
        
        # Créer un client
        self.guest = Guest.objects.create(
            name='John Doe',
            sex='M',
            type_of_id='Passport',
            id_number='TEST123456',
            contact_number='+243999999999',
            email='john@test.com'
        )
        
        # Créer une réservation multi-chambres
        self.reservation = Reservation.objects.create(
            guest=self.guest,
            people_count=3,
            keys_count=3,
            check_in=datetime.now(),
            number_of_days=5,
            status='checked_in'
        )
        
        # Associer les chambres
        self.res_room1 = ReservationRoom.objects.create(
            reservation=self.reservation,
            room=self.room1,
            price_per_day=50.00
        )
        self.res_room2 = ReservationRoom.objects.create(
            reservation=self.reservation,
            room=self.room2,
            price_per_day=50.00
        )
        self.res_room3 = ReservationRoom.objects.create(
            reservation=self.reservation,
            room=self.room3,
            price_per_day=50.00
        )
        
        # Mettre les chambres en statut "occupied"
        self.room1.status = 'occupied'
        self.room1.save()
        self.room2.status = 'occupied'
        self.room2.save()
        self.room3.status = 'occupied'
        self.room3.save()
    
    def test_release_single_room_success(self):
        """Test: Libérer une chambre avec succès"""
        url = f'/api/reservations/{self.reservation.id}/release-room/'
        data = {
            'room_id': self.room1.id,
            'reason': 'Client parti plus tôt'
        }
        
        response = self.client.post(url, data, format='json')
        
        # Vérifications
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['room_released'], True)
        self.assertEqual(response.data['remaining_rooms'], 2)
        self.assertIn('Chambre 101 libérée', response.data['message'])
        
        # Vérifier que la chambre est disponible
        self.room1.refresh_from_db()
        self.assertEqual(self.room1.status, 'available')
        
        # Vérifier que la réservation est toujours active
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.status, 'checked_in')
        
        # Vérifier que ReservationRoom a été supprimé
        self.assertFalse(
            ReservationRoom.objects.filter(id=self.res_room1.id).exists()
        )
    
    def test_release_last_room_completes_reservation(self):
        """Test: Libérer la dernière chambre termine la réservation"""
        # Libérer les deux premières chambres
        url = f'/api/reservations/{self.reservation.id}/release-room/'
        
        self.client.post(url, {'room_id': self.room1.id}, format='json')
        self.client.post(url, {'room_id': self.room2.id}, format='json')
        
        # Libérer la dernière chambre
        response = self.client.post(
            url, 
            {'room_id': self.room3.id, 'reason': 'Checkout final'}, 
            format='json'
        )
        
        # Vérifications
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['reservation_completed'], True)
        self.assertIn('dernière chambre', response.data['message'].lower())
        
        # Vérifier que la réservation est terminée
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.status, 'checked_out')
        
        # Vérifier que toutes les chambres sont disponibles
        self.room1.refresh_from_db()
        self.room2.refresh_from_db()
        self.room3.refresh_from_db()
        self.assertEqual(self.room1.status, 'available')
        self.assertEqual(self.room2.status, 'available')
        self.assertEqual(self.room3.status, 'available')
        
        # Vérifier qu'il n'y a plus de ReservationRoom
        self.assertEqual(
            ReservationRoom.objects.filter(reservation=self.reservation).count(),
            0
        )
    
    def test_cannot_release_room_from_wrong_reservation(self):
        """Test: Impossible de libérer une chambre d'une autre réservation"""
        # Créer une autre chambre non associée
        other_room = Room.objects.create(
            number='201',
            type=self.room_type,
            floor=self.floor,
            status='available'
        )
        
        url = f'/api/reservations/{self.reservation.id}/release-room/'
        data = {'room_id': other_room.id}
        
        response = self.client.post(url, data, format='json')
        
        # Vérifications
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('pas associée', response.data['error'])
    
    def test_cannot_release_room_with_invalid_status(self):
        """Test: Impossible de libérer une chambre si statut invalide"""
        # Annuler la réservation
        self.reservation.status = 'cancelled'
        self.reservation.save()
        
        url = f'/api/reservations/{self.reservation.id}/release-room/'
        data = {'room_id': self.room1.id}
        
        response = self.client.post(url, data, format='json')
        
        # Vérifications
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Impossible de libérer', response.data['error'])
    
    def test_release_room_without_room_id(self):
        """Test: Erreur si room_id manquant"""
        url = f'/api/reservations/{self.reservation.id}/release-room/'
        data = {'reason': 'Test'}
        
        response = self.client.post(url, data, format='json')
        
        # Vérifications
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('requis', response.data['error'])
    
    def test_total_price_recalculation_after_release(self):
        """Test: Vérifier que total_price est recalculé après libération"""
        # Prix initial: 3 chambres × 50 FC × 5 jours = 750 FC
        initial_price = self.reservation.total_price
        self.assertEqual(initial_price, 750.00)
        
        # Libérer une chambre
        url = f'/api/reservations/{self.reservation.id}/release-room/'
        self.client.post(url, {'room_id': self.room1.id}, format='json')
        
        # Nouveau prix: 2 chambres × 50 FC × 5 jours = 500 FC
        self.reservation.refresh_from_db()
        new_price = self.reservation.total_price
        self.assertEqual(new_price, 500.00)


class ReservationCancellationTestCase(TestCase):
    """Tests pour l'annulation de réservations"""
    
    def setUp(self):
        """Configuration initiale"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Créer les objets nécessaires
        self.floor = Floor.objects.create(name='1er Étage', floor_number=1)
        self.room_type = RoomType.objects.create(
            name='Standard',
            base_price=50.00,
            capacity=2
        )
        
        self.room1 = Room.objects.create(
            number='101',
            type=self.room_type,
            floor=self.floor,
            status='occupied'
        )
        self.room2 = Room.objects.create(
            number='102',
            type=self.room_type,
            floor=self.floor,
            status='occupied'
        )
        
        self.guest = Guest.objects.create(
            name='Jane Smith',
            sex='F',
            type_of_id='ID Card',
            id_number='ID789',
            contact_number='+243888888888'
        )
        
        self.reservation = Reservation.objects.create(
            guest=self.guest,
            people_count=2,
            keys_count=2,
            check_in=datetime.now(),
            number_of_days=3,
            status='confirmed'
        )
        
        ReservationRoom.objects.create(
            reservation=self.reservation,
            room=self.room1,
            price_per_day=50.00
        )
        ReservationRoom.objects.create(
            reservation=self.reservation,
            room=self.room2,
            price_per_day=50.00
        )
    
    def test_cancel_reservation_success(self):
        """Test: Annuler une réservation avec succès"""
        url = f'/api/reservations/{self.reservation.id}/'
        
        response = self.client.delete(url)
        
        # Vérifications
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('annulée avec succès', response.data['message'])
        self.assertEqual(len(response.data['rooms_released']), 2)
        self.assertIn('101', response.data['rooms_released'])
        self.assertIn('102', response.data['rooms_released'])
        
        # Vérifier que la réservation est annulée
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.status, 'cancelled')
        
        # Vérifier que les chambres sont disponibles
        self.room1.refresh_from_db()
        self.room2.refresh_from_db()
        self.assertEqual(self.room1.status, 'available')
        self.assertEqual(self.room2.status, 'available')
    
    def test_cannot_cancel_checked_out_reservation(self):
        """Test: Impossible d'annuler une réservation terminée"""
        self.reservation.status = 'checked_out'
        self.reservation.save()
        
        url = f'/api/reservations/{self.reservation.id}/'
        response = self.client.delete(url)
        
        # Vérifications
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Impossible', response.data['error'])
    
    def test_cannot_cancel_already_cancelled_reservation(self):
        """Test: Impossible d'annuler une réservation déjà annulée"""
        self.reservation.status = 'cancelled'
        self.reservation.save()
        
        url = f'/api/reservations/{self.reservation.id}/'
        response = self.client.delete(url)
        
        # Vérifications
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Impossible', response.data['error'])
    
    def test_cancel_reservation_with_payment(self):
        """Test: Annuler une réservation avec paiement (montant conservé)"""
        # Ajouter un paiement
        self.reservation.paid_amount = 100.00
        self.reservation.payment_status = 'partial'
        self.reservation.save()
        
        url = f'/api/reservations/{self.reservation.id}/'
        response = self.client.delete(url)
        
        # Vérifications
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Vérifier que le montant payé est conservé
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.paid_amount, 100.00)
        self.assertEqual(self.reservation.status, 'cancelled')
    
    def test_cancel_nonexistent_reservation(self):
        """Test: Erreur si réservation n'existe pas"""
        url = '/api/reservations/99999/'
        response = self.client.delete(url)
        
        # Vérifications
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('non trouvée', response.data['error'])


class IntegrationTestCase(TestCase):
    """Tests d'intégration combinant plusieurs opérations"""
    
    def setUp(self):
        """Configuration"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Créer les objets
        self.floor = Floor.objects.create(name='1er Étage', floor_number=1)
        self.room_type = RoomType.objects.create(
            name='Standard',
            base_price=50.00,
            capacity=2
        )
        
        self.rooms = [
            Room.objects.create(
                number=f'10{i}',
                type=self.room_type,
                floor=self.floor,
                status='available'
            )
            for i in range(1, 4)
        ]
        
        self.guest = Guest.objects.create(
            name='Test Guest',
            sex='M',
            type_of_id='Passport',
            id_number='INTEG123',
            contact_number='+243777777777'
        )
    
    def test_full_lifecycle_with_partial_release(self):
        """Test: Cycle complet avec libération partielle"""
        # 1. Créer une réservation avec 3 chambres
        reservation = Reservation.objects.create(
            guest=self.guest,
            people_count=3,
            keys_count=3,
            check_in=datetime.now(),
            number_of_days=5,
            status='confirmed'
        )
        
        for room in self.rooms:
            ReservationRoom.objects.create(
                reservation=reservation,
                room=room,
                price_per_day=50.00
            )
            room.status = 'occupied'
            room.save()
        
        # Vérifier le prix initial
        self.assertEqual(reservation.total_price, 750.00)  # 3 × 50 × 5
        
        # 2. Libérer une chambre
        url = f'/api/reservations/{reservation.id}/release-room/'
        response = self.client.post(
            url, 
            {'room_id': self.rooms[0].id}, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Vérifier le nouveau prix
        reservation.refresh_from_db()
        self.assertEqual(reservation.total_price, 500.00)  # 2 × 50 × 5
        
        # 3. Ajouter un paiement
        Payment.objects.create(
            reservation=reservation,
            amount=300.00,
            payment_method='cash',
            payment_date=datetime.now(),
            created_by=self.user
        )
        reservation.paid_amount = 300.00
        reservation.payment_status = 'partial'
        reservation.save()
        
        # 4. Libérer les chambres restantes
        self.client.post(url, {'room_id': self.rooms[1].id}, format='json')
        response = self.client.post(url, {'room_id': self.rooms[2].id}, format='json')
        
        # Vérifier que la réservation est terminée
        self.assertEqual(response.data['reservation_completed'], True)
        reservation.refresh_from_db()
        self.assertEqual(reservation.status, 'checked_out')
        
        # Vérifier que toutes les chambres sont disponibles
        for room in self.rooms:
            room.refresh_from_db()
            self.assertEqual(room.status, 'available')


# Lancer les tests avec:
# python manage.py test reservation.tests
