from rest_framework import serializers
from .models import Guest, Reservation, ReservationRoom, Payment
from rooms.models import Room
from django.db import transaction


class GuestSerializer(serializers.ModelSerializer):
    """Serializer for Guest model"""
    class Meta:
        model = Guest
        fields = ['id', 'name', 'sex', 'type_of_id', 'id_number', 'contact_number', 'email']


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model"""
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    created_by_role = serializers.CharField(source='created_by.profile.role', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'amount', 'payment_method', 'payment_method_display',
            'payment_date', 'reference_number', 'notes', 
            'created_by_username', 'created_by_role', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'created_by_username', 'created_by_role']


class ReservationRoomSerializer(serializers.ModelSerializer):
    """Serializer for ReservationRoom model"""
    room_id = serializers.IntegerField(source='room.id', read_only=True)
    room_number = serializers.CharField(source='room.number', read_only=True)
    room_type = serializers.CharField(source='room.type.name', read_only=True)
    room_status = serializers.CharField(source='room.status', read_only=True)
    
    class Meta:
        model = ReservationRoom
        fields = ['id', 'room', 'room_id', 'room_number', 'room_type', 'room_status', 'price_per_day', 'notes']
        read_only_fields = ['id']


class ReservationRoomCreateSerializer(serializers.Serializer):
    """Serializer for creating a reservation room"""
    room_id = serializers.IntegerField()
    notes = serializers.CharField(required=False, allow_blank=True)


class ReservationCreateSerializer(serializers.Serializer):
    """Serializer for creating a reservation with multiple rooms"""
    # Guest information
    guest_name = serializers.CharField(max_length=100)
    guest_sex = serializers.ChoiceField(choices=[('M', 'Masculin'), ('F', 'Féminin')])
    guest_type_of_id = serializers.CharField(max_length=50)
    guest_id_number = serializers.CharField(max_length=50)
    guest_contact_number = serializers.CharField(max_length=20)
    guest_email = serializers.EmailField(required=False, allow_blank=True)
    
    # Reservation details
    people_count = serializers.IntegerField(min_value=1)
    keys_count = serializers.IntegerField(min_value=1)
    check_in = serializers.DateTimeField()
    number_of_days = serializers.IntegerField(min_value=1)
    check_out_date = serializers.DateField(required=False, allow_null=True)
    check_out_time = serializers.TimeField(required=False, allow_null=True)
    
    # Payment
    paid_amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = serializers.ChoiceField(
        choices=[
            ('cash', 'Espèces'),
            ('mobile_money', 'Mobile Money'),
            ('bank_transfer', 'Virement Bancaire'),
            ('credit_card', 'Carte de Crédit'),
            ('check', 'Chèque'),
        ],
        required=False,
        default='cash'
    )
    payment_status = serializers.ChoiceField(
        choices=Reservation.PAYMENT_STATUS,
        default='unpaid'
    )
    
    # Rooms
    rooms = ReservationRoomCreateSerializer(many=True)
    
    def validate_rooms(self, value):
        """Validate that all rooms exist and are available"""
        if not value:
            raise serializers.ValidationError("Au moins une chambre doit être sélectionnée.")
        
        room_ids = [room['room_id'] for room in value]
        
        # Vérifier que toutes les chambres existent
        rooms = Room.objects.filter(id__in=room_ids)
        if rooms.count() != len(room_ids):
            raise serializers.ValidationError("Une ou plusieurs chambres n'existent pas.")
        
        # Vérifier que toutes les chambres sont disponibles (status = 'available')
        unavailable_rooms = rooms.exclude(status='available')
        if unavailable_rooms.exists():
            unavailable_numbers = [
                f"{room.number} ({room.get_status_display()})" 
                for room in unavailable_rooms
            ]
            raise serializers.ValidationError(
                f"Les chambres suivantes ne sont pas disponibles : {', '.join(unavailable_numbers)}"
            )
        
        return value
    
    def validate_guest_id_number(self, value):
        """Check if guest already exists"""
        return value
    
    @transaction.atomic
    def create(self, validated_data):
        """Create reservation with multiple rooms"""
        # Extract rooms data
        rooms_data = validated_data.pop('rooms')
        
        # Extract guest data
        guest_data = {
            'name': validated_data.pop('guest_name'),
            'sex': validated_data.pop('guest_sex'),
            'type_of_id': validated_data.pop('guest_type_of_id'),
            'id_number': validated_data.pop('guest_id_number'),
            'contact_number': validated_data.pop('guest_contact_number'),
            'email': validated_data.pop('guest_email', ''),
        }
        
        # Get or create guest
        guest, created = Guest.objects.get_or_create(
            id_number=guest_data['id_number'],
            defaults=guest_data
        )
        
        # Extract paid_amount before creating reservation
        paid_amount = validated_data.get('paid_amount', 0)
        payment_method = validated_data.pop('payment_method', 'cash')
        
        # Get current user from context
        request = self.context.get('request')
        current_user = request.user if request and request.user.is_authenticated else None
        
        # Create reservation
        reservation = Reservation.objects.create(
            guest=guest,
            created_by=current_user,
            **validated_data
        )
        
        # Create reservation rooms and mark rooms as occupied
        for room_data in rooms_data:
            room = Room.objects.get(id=room_data['room_id'])
            
            ReservationRoom.objects.create(
                reservation=reservation,
                room=room,
                price_per_day=room.type.price_per_night,
                notes=room_data.get('notes', '')
            )
            
            # Mark room as occupied
            room.status = 'occupied'
            room.save()
        
        # Create initial Payment record if amount > 0
        if paid_amount > 0:
            from datetime import datetime
            Payment.objects.create(
                reservation=reservation,
                amount=paid_amount,
                payment_method=payment_method,
                payment_date=reservation.check_in,
                notes='Paiement initial lors de la réservation',
                created_by=current_user
            )
        
        return reservation


class ReservationDetailSerializer(serializers.ModelSerializer):
    """Serializer for viewing reservation details"""
    guest = GuestSerializer(read_only=True)
    reservation_rooms = ReservationRoomSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    remaining_amount = serializers.SerializerMethodField()
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    created_by_role = serializers.CharField(source='created_by.profile.role', read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'guest', 'people_count', 'keys_count',
            'check_in', 'number_of_days', 'check_out_date', 'check_out_time',
            'status', 'payment_status', 'paid_amount', 'total_price',
            'remaining_amount', 'reservation_rooms', 'payments',
            'created_by_username', 'created_by_role',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'check_out_date', 'check_out_time', 'created_at', 'updated_at']
    
    def get_remaining_amount(self, obj):
        """Calculate remaining amount to pay"""
        return obj.total_price - obj.paid_amount


class ReservationListSerializer(serializers.ModelSerializer):
    """Serializer for listing reservations"""
    guest_name = serializers.CharField(source='guest.name', read_only=True)
    rooms_count = serializers.SerializerMethodField()
    total_price = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    created_by_role = serializers.CharField(source='created_by.profile.role', read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'guest_name', 'people_count', 'rooms_count',
            'check_in', 'check_out_date', 'number_of_days',
            'status', 'payment_status', 'paid_amount', 'total_price',
            'created_by_username', 'created_by_role',
            'created_at'
        ]
    
    def get_rooms_count(self, obj):
        """Get number of rooms in reservation"""
        return obj.reservation_rooms.count()


class RoomChangeSerializer(serializers.Serializer):
    """Serializer for room change/exchange"""
    reservation_id = serializers.IntegerField(help_text="ID of the reservation")
    old_room_id = serializers.IntegerField(help_text="ID of the current room")
    new_room_id = serializers.IntegerField(help_text="ID of the new room")
    reason = serializers.CharField(required=False, allow_blank=True, help_text="Reason for room change")
    
    # Payment fields for exchange fee
    exchange_fee = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=False, 
        allow_null=True,
        help_text="Fee charged for room exchange"
    )
    payment_method = serializers.ChoiceField(
        choices=Payment.PAYMENT_METHOD_CHOICES,
        required=False,
        allow_blank=True,
        help_text="Payment method for exchange fee"
    )
    payment_reference = serializers.CharField(
        required=False, 
        allow_blank=True,
        help_text="Reference number for the payment"
    )
    payment_notes = serializers.CharField(
        required=False, 
        allow_blank=True,
        help_text="Notes for the payment"
    )
    
    def validate(self, data):
        """Validate room change data"""
        # Check if reservation exists
        try:
            reservation = Reservation.objects.get(id=data['reservation_id'])
        except Reservation.DoesNotExist:
            raise serializers.ValidationError("Réservation introuvable.")
        
        # Check if old room exists and belongs to reservation
        try:
            old_room = Room.objects.get(id=data['old_room_id'])
            old_reservation_room = ReservationRoom.objects.get(
                reservation=reservation,
                room=old_room
            )
        except Room.DoesNotExist:
            raise serializers.ValidationError("Ancienne chambre introuvable.")
        except ReservationRoom.DoesNotExist:
            raise serializers.ValidationError("Cette chambre n'appartient pas à cette réservation.")
        
        # Check if new room exists and is available
        try:
            new_room = Room.objects.get(id=data['new_room_id'])
            if new_room.status != 'available':
                raise serializers.ValidationError(f"La nouvelle chambre {new_room.number} n'est pas disponible.")
        except Room.DoesNotExist:
            raise serializers.ValidationError("Nouvelle chambre introuvable.")
        
        # Check if trying to change to the same room
        if data['old_room_id'] == data['new_room_id']:
            raise serializers.ValidationError("La nouvelle chambre doit être différente de l'ancienne.")
        
        # If exchange fee is provided, payment method must be provided
        if data.get('exchange_fee') and data['exchange_fee'] > 0:
            if not data.get('payment_method'):
                raise serializers.ValidationError("La méthode de paiement est requise si des frais sont appliqués.")
        
        return data
    
    @transaction.atomic
    def save(self, **kwargs):
        """Perform room change"""
        user = kwargs.get('user')
        reservation = Reservation.objects.get(id=self.validated_data['reservation_id'])
        old_room = Room.objects.get(id=self.validated_data['old_room_id'])
        new_room = Room.objects.get(id=self.validated_data['new_room_id'])
        
        # Get the reservation room entry
        reservation_room = ReservationRoom.objects.get(
            reservation=reservation,
            room=old_room
        )
        
        # Update room statuses
        old_room.status = 'available'
        old_room.save()
        
        new_room.status = 'occupied'
        new_room.save()
        
        # Update the reservation room
        reservation_room.room = new_room
        reservation_room.price_per_day = new_room.type.price_per_night
        
        # Add reason to notes if provided
        reason = self.validated_data.get('reason', '')
        if reason:
            existing_notes = reservation_room.notes or ''
            change_note = f"[Échange de chambre] {old_room.number} → {new_room.number}. Motif: {reason}"
            reservation_room.notes = f"{existing_notes}\n{change_note}" if existing_notes else change_note
        
        reservation_room.save()
        
        # Create payment record if exchange fee is provided
        payment = None
        exchange_fee = self.validated_data.get('exchange_fee')
        if exchange_fee and exchange_fee > 0:
            from django.utils import timezone
            
            payment = Payment.objects.create(
                reservation=reservation,
                amount=exchange_fee,
                payment_method=self.validated_data.get('payment_method'),
                payment_date=timezone.now(),
                reference_number=self.validated_data.get('payment_reference', ''),
                notes=self.validated_data.get('payment_notes') or f"Frais d'échange de chambre {old_room.number} → {new_room.number}",
                created_by=user
            )
            
            # Update reservation paid amount
            reservation.paid_amount += exchange_fee
            reservation.save()
        
        return {
            'reservation': reservation,
            'old_room': old_room,
            'new_room': new_room,
            'payment': payment
        }
