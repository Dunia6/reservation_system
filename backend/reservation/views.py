from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Reservation, Guest, ReservationRoom, Payment
from .serializers import (
    ReservationCreateSerializer,
    ReservationDetailSerializer,
    ReservationListSerializer,
    GuestSerializer,
    RoomChangeSerializer
)
from core.permissions import IsManager, IsSuperviseur, IsManagerOrSuperviseur


class ReservationViewSet(viewsets.GenericViewSet):
    """
    ViewSet for managing reservations
    
    list: Get all reservations
    create: Create a new reservation with multiple rooms
    retrieve: Get details of a specific reservation
    update: Update reservation details
    destroy: Cancel a reservation (Manager et Superviseur uniquement)
    """
    queryset = Reservation.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """Permissions par action: destroy et dashboard_stats restreints"""

        if self.action == 'destroy':
            # Seuls Manager et Superviseur peuvent annuler
            return [IsManagerOrSuperviseur()]
        elif self.action == 'dashboard_stats':
            # Seul Superviseur peut accéder aux statistiques
            return [IsSuperviseur()]
        # Tous les autres actions: tous les utilisateurs authentifiés
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ReservationCreateSerializer
        elif self.action == 'retrieve':
            return ReservationDetailSerializer
        return ReservationListSerializer
    
    @swagger_auto_schema(
        operation_description="Get list of all reservations",
        responses={200: ReservationListSerializer(many=True)},
        tags=['Reservations']
    )
    def list(self, request):
        """Get all reservations"""
        queryset = self.get_queryset().select_related('guest').prefetch_related('reservation_rooms')
        
        # Filter by status
        status_filter = request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by payment status
        payment_status = request.query_params.get('payment_status', None)
        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)
        
        # Search by guest name
        search = request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(guest__name__icontains=search) |
                Q(guest__id_number__icontains=search)
            )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Create a new reservation with multiple rooms",
        request_body=ReservationCreateSerializer,
        responses={
            201: ReservationDetailSerializer,
            400: 'Bad Request - Validation errors'
        },
        tags=['Reservations']
    )
    def create(self, request):
        """Create a new reservation with multiple rooms"""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            reservation = serializer.save()
            
            # Return detailed reservation
            detail_serializer = ReservationDetailSerializer(reservation)
            return Response(
                detail_serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @swagger_auto_schema(
        operation_description="Get details of a specific reservation",
        responses={
            200: ReservationDetailSerializer,
            404: 'Reservation not found'
        },
        tags=['Reservations']
    )
    def retrieve(self, request, pk=None):
        """Get reservation details"""
        try:
            reservation = self.get_queryset().select_related('guest').prefetch_related(
                'reservation_rooms__room__type',
                'reservation_rooms__room__floor'
            ).get(pk=pk)
            
            serializer = self.get_serializer(reservation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Reservation.DoesNotExist:
            return Response(
                {"error": "Réservation non trouvée."},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @swagger_auto_schema(
        operation_description="Update reservation status",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['pending', 'confirmed', 'checked_in', 'checked_out', 'cancelled']
                )
            }
        ),
        responses={200: ReservationDetailSerializer},
        tags=['Reservations']
    )
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update reservation status"""
        try:
            reservation = self.get_queryset().get(pk=pk)
            new_status = request.data.get('status')
            
            if new_status not in dict(Reservation.STATUS_CHOICES):
                return Response(
                    {"error": "Statut invalide."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            reservation.status = new_status
            reservation.save()
            
            serializer = ReservationDetailSerializer(reservation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Reservation.DoesNotExist:
            return Response(
                {"error": "Réservation non trouvée."},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @swagger_auto_schema(
        operation_description="Add payment to reservation",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Amount to add')
            },
            required=['amount']
        ),
        responses={200: ReservationDetailSerializer},
        tags=['Reservations']
    )
    @action(detail=True, methods=['post'])
    def add_payment(self, request, pk=None):
        """Add payment to reservation"""
        try:
            reservation = self.get_queryset().get(pk=pk)
            amount = float(request.data.get('amount', 0))
            
            if amount <= 0:
                return Response(
                    {"error": "Le montant doit être supérieur à 0."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            reservation.paid_amount += amount
            
            # Update payment status
            if reservation.paid_amount >= reservation.total_price:
                reservation.payment_status = 'paid'
            elif reservation.paid_amount > 0:
                reservation.payment_status = 'partial'
            
            reservation.save()
            
            serializer = ReservationDetailSerializer(reservation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Reservation.DoesNotExist:
            return Response(
                {"error": "Réservation non trouvée."},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @swagger_auto_schema(
        operation_description="Add a payment to a reservation",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['amount', 'payment_method', 'payment_date'],
            properties={
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Payment amount'),
                'payment_method': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['cash', 'mobile_money', 'bank_transfer', 'credit_card', 'check'],
                    description='Payment method'
                ),
                'payment_date': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='Payment date'),
                'reference_number': openapi.Schema(type=openapi.TYPE_STRING, description='Reference number (optional)'),
                'notes': openapi.Schema(type=openapi.TYPE_STRING, description='Additional notes (optional)')
            }
        ),
        responses={
            200: ReservationDetailSerializer,
            400: 'Bad Request - Invalid payment data',
            404: 'Reservation not found'
        },
        tags=['Reservations']
    )
    @action(detail=True, methods=['post'])
    def add_payment(self, request, pk=None):
        """Add a payment to a reservation"""
        try:
            reservation = self.get_queryset().get(pk=pk)
            
            amount = request.data.get('amount')
            payment_method = request.data.get('payment_method')
            
            # Validate amount
            if not amount or float(amount) <= 0:
                return Response(
                    {"error": "Le montant doit être supérieur à 0."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            from decimal import Decimal
            amount = Decimal(str(amount))
            
            # Check if amount exceeds remaining amount
            if amount > reservation.remaining_amount:
                return Response(
                    {"error": f"Le montant ne peut pas dépasser le reste à payer ({reservation.remaining_amount} FC)."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create Payment record
            payment = Payment.objects.create(
                reservation=reservation,
                amount=amount,
                payment_method=payment_method,
                payment_date=request.data.get('payment_date'),
                reference_number=request.data.get('reference_number', ''),
                notes=request.data.get('notes', ''),
                created_by=request.user if request.user.is_authenticated else None
            )
            
            # Update paid amount
            reservation.paid_amount += amount
            
            # Update payment status
            if reservation.paid_amount >= reservation.total_price:
                reservation.payment_status = 'paid'
            elif reservation.paid_amount > 0:
                reservation.payment_status = 'partial'
            else:
                reservation.payment_status = 'unpaid'
            
            reservation.save()
            
            serializer = ReservationDetailSerializer(reservation)
            return Response(
                {
                    "message": "Paiement ajouté avec succès.",
                    "reservation": serializer.data
                },
                status=status.HTTP_200_OK
            )
        
        except Reservation.DoesNotExist:
            return Response(
                {"error": "Réservation non trouvée."},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {"error": "Montant invalide."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @swagger_auto_schema(
        operation_description="Cancel a reservation and release all rooms",
        responses={
            200: 'Reservation cancelled successfully',
            400: 'Bad Request - Cannot cancel reservation',
            404: 'Reservation not found'
        },
        tags=['Reservations']
    )
    def destroy(self, request, pk=None):
        """Cancel reservation and release all rooms"""
        try:
            reservation = self.get_queryset().get(pk=pk)
            
            # Check if reservation can be cancelled
            if reservation.status in ['checked_out', 'cancelled']:
                return Response(
                    {"error": f"Impossible d'annuler une réservation avec le statut '{reservation.get_status_display()}'."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Release all rooms and set status back to available
            rooms_released = []
            for reservation_room in reservation.reservation_rooms.all():
                room = reservation_room.room
                room.status = 'available'
                room.save()
                rooms_released.append(room.number)
            
            # Update reservation status
            reservation.status = 'cancelled'
            reservation.save()
            
            return Response(
                {
                    "message": "Réservation annulée avec succès.",
                    "rooms_released": rooms_released,
                    "reservation_id": reservation.id
                },
                status=status.HTTP_200_OK
            )
        
        except Reservation.DoesNotExist:
            return Response(
                {"error": "Réservation non trouvée."},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @swagger_auto_schema(
        operation_description="Release a specific room from a reservation",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['room_id'],
            properties={
                'room_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the room to release'
                ),
                'reason': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Reason for releasing the room (optional)'
                )
            }
        ),
        responses={
            200: ReservationDetailSerializer,
            400: 'Bad Request - Cannot release room',
            404: 'Reservation or room not found'
        },
        tags=['Reservations']
    )
    @action(detail=True, methods=['post'], url_path='release-room')
    def release_room(self, request, pk=None):
        """Release a specific room from a reservation"""
        try:
            reservation = self.get_queryset().get(pk=pk)
            room_id = request.data.get('room_id')
            reason = request.data.get('reason', '')
            
            if not room_id:
                return Response(
                    {"error": "L'ID de la chambre est requis."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Find the reservation room
            try:
                reservation_room = reservation.reservation_rooms.get(room_id=room_id)
            except ReservationRoom.DoesNotExist:
                return Response(
                    {"error": "Cette chambre n'est pas associée à cette réservation."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Check if reservation status allows room release
            if reservation.status not in ['confirmed', 'checked_in']:
                return Response(
                    {"error": f"Impossible de libérer une chambre pour une réservation avec le statut '{reservation.get_status_display()}'."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Release the room
            room = reservation_room.room
            room.status = 'available'
            room.save()
            
            # Check if this was the last room in the reservation
            remaining_rooms = reservation.reservation_rooms.exclude(id=reservation_room.id).count()
            
            if remaining_rooms == 0:
                # If no rooms left, update reservation status to checked_out
                reservation.status = 'checked_out'
                reservation.save()
                
                # Remove the reservation room record
                reservation_room.delete()
                
                return Response(
                    {
                        "message": "Dernière chambre libérée. La réservation a été marquée comme terminée.",
                        "room_number": room.number,
                        "room_released": True,
                        "reservation_completed": True,
                        "reservation": ReservationDetailSerializer(reservation).data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                # Remove the reservation room record
                reservation_room.delete()
                
                # Recalculate paid_amount if needed (proportional adjustment)
                # This is optional - you may want to keep the paid amount as is
                
                return Response(
                    {
                        "message": f"Chambre {room.number} libérée avec succès.",
                        "room_number": room.number,
                        "room_released": True,
                        "remaining_rooms": remaining_rooms,
                        "reason": reason,
                        "reservation": ReservationDetailSerializer(reservation).data
                    },
                    status=status.HTTP_200_OK
                )
        
        except Reservation.DoesNotExist:
            return Response(
                {"error": "Réservation non trouvée."},
                status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        operation_description="Get all payments history",
        manual_parameters=[
            openapi.Parameter('limit', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Number of payments to return (default: 50)')
        ],
        responses={200: 'List of recent payments'},
        tags=['Reservations']
    )
    @action(detail=False, methods=['get'], url_path='payments-history')
    def payments_history(self, request):
        """Get recent payments history"""
        limit = int(request.query_params.get('limit', 50))
        
        payments = Payment.objects.select_related(
            'reservation', 
            'reservation__guest',
            'created_by',
            'created_by__profile'
        ).prefetch_related(
            'reservation__reservation_rooms__room'
        ).order_by('-payment_date')[:limit]
        
        payments_data = []
        for payment in payments:
            # Get room numbers for this reservation
            room_numbers = [
                rr.room.number 
                for rr in payment.reservation.reservation_rooms.all()
            ]
            
            payments_data.append({
                'id': payment.id,
                'amount': str(payment.amount),
                'payment_method': payment.payment_method,
                'payment_method_display': payment.get_payment_method_display(),
                'payment_date': payment.payment_date,
                'reference_number': payment.reference_number,
                'notes': payment.notes,
                'reservation_id': payment.reservation.id,
                'guest_name': payment.reservation.guest.name,
                'room_numbers': room_numbers,
                'created_by_username': payment.created_by.username if payment.created_by else None,
                'created_by_role': payment.created_by.profile.role if payment.created_by and hasattr(payment.created_by, 'profile') else None,
                'created_at': payment.created_at,
            })
        
        return Response(payments_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get dashboard statistics",
        responses={200: 'Dashboard statistics'},
        tags=['Reservations']
    )
    @action(detail=False, methods=['get'], url_path='dashboard-stats')
    def dashboard_stats(self, request):
        """Get statistics for dashboard"""
        from django.utils import timezone
        from datetime import timedelta
        from django.db.models import Sum
        
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=now.weekday())
        month_start = today_start.replace(day=1)
        
        # Today's revenue
        today_payments = Payment.objects.filter(
            payment_date__gte=today_start
        ).aggregate(total=Sum('amount'))
        today_revenue = today_payments['total'] or 0
        today_reservations = Reservation.objects.filter(
            created_at__gte=today_start
        ).count()
        
        # This week's revenue
        week_payments = Payment.objects.filter(
            payment_date__gte=week_start
        ).aggregate(total=Sum('amount'))
        week_revenue = week_payments['total'] or 0
        week_reservations = Reservation.objects.filter(
            created_at__gte=week_start
        ).count()
        
        # This month's revenue
        month_payments = Payment.objects.filter(
            payment_date__gte=month_start
        ).aggregate(total=Sum('amount'))
        month_revenue = month_payments['total'] or 0
        month_reservations = Reservation.objects.filter(
            created_at__gte=month_start
        ).count()
        
        return Response({
            'today': {
                'revenue': str(today_revenue),
                'reservations': today_reservations
            },
            'week': {
                'revenue': str(week_revenue),
                'reservations': week_reservations
            },
            'month': {
                'revenue': str(month_revenue),
                'reservations': month_reservations
            }
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Change room for a reservation",
        request_body=RoomChangeSerializer,
        responses={
            200: 'Room changed successfully',
            400: 'Bad Request - Validation errors'
        },
        tags=['Reservations']
    )
    @action(detail=False, methods=['post'], url_path='change-room')
    def change_room(self, request):
        """Change room for a reservation"""
        serializer = RoomChangeSerializer(data=request.data)
        
        if serializer.is_valid():
            result = serializer.save(user=request.user)
            
            response_data = {
                'message': 'Échange de chambre effectué avec succès.',
                'reservation_id': result['reservation'].id,
                'old_room': {
                    'id': result['old_room'].id,
                    'number': result['old_room'].number
                },
                'new_room': {
                    'id': result['new_room'].id,
                    'number': result['new_room'].number
                }
            }
            
            if result['payment']:
                response_data['payment'] = {
                    'id': result['payment'].id,
                    'amount': str(result['payment'].amount),
                    'payment_method': result['payment'].get_payment_method_display()
                }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GuestViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing guests"""
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Search guests by name or ID number",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, type=openapi.TYPE_STRING)
        ],
        responses={200: GuestSerializer(many=True)},
        tags=['Guests']
    )
    def list(self, request):
        """Get all guests with optional search"""
        queryset = self.get_queryset()
        
        search = request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(id_number__icontains=search) |
                Q(contact_number__icontains=search)
            )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
