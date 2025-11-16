from rest_framework import serializers
from .models import Room, RoomType, Floor


class FloorSerializer(serializers.ModelSerializer):
    """ Serializer for Floor model. """
    class Meta:
        model = Floor
        fields = ['id', 'number']
        

class RoomTypeSerializer(serializers.ModelSerializer):
    """ Serializer for RoomType model. """
    class Meta:
        model = RoomType
        fields = ['id', 'name', 'price_per_night']


class RoomSerializer(serializers.ModelSerializer):
    """ Serializer for Room model. """
    floor = FloorSerializer(read_only=True)
    type = RoomTypeSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    # Write-only fields for creating/updating
    floor_id = serializers.PrimaryKeyRelatedField(
        queryset=Floor.objects.all(), 
        source='floor', 
        write_only=True,
        required=False
    )
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=RoomType.objects.all(), 
        source='type', 
        write_only=True,
        required=False
    )

    class Meta:
        model = Room
        fields = ['id', 'number', 'floor', 'type', 'is_available', 'status', 'status_display', 
                  'floor_id', 'type_id']


class RoomDetailSerializer(serializers.ModelSerializer):
    """ Detailed serializer for Room model with active reservation. """
    floor = FloorSerializer(read_only=True)
    type = RoomTypeSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    active_reservation = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id', 'number', 'floor', 'type', 'is_available', 'status', 'status_display', 'active_reservation']

    def get_active_reservation(self, obj):
        """Get active reservation for this room if any"""
        from reservation.models import ReservationRoom
        
        # Get the most recent reservation room that's not cancelled
        reservation_room = ReservationRoom.objects.filter(
            room=obj,
            reservation__status__in=['pending', 'confirmed', 'checked_in']
        ).select_related(
            'reservation__guest'
        ).order_by('-reservation__created_at').first()
        
        if not reservation_room:
            return None
        
        reservation = reservation_room.reservation
        
        return {
            'id': reservation.id,
            'guest': {
                'id': reservation.guest.id,
                'name': reservation.guest.name,
                'sex': reservation.guest.get_sex_display(),
                'type_of_id': reservation.guest.type_of_id,
                'id_number': reservation.guest.id_number,
                'contact_number': reservation.guest.contact_number,
                'email': reservation.guest.email,
            },
            'people_count': reservation.people_count,
            'keys_count': reservation.keys_count,
            'check_in': reservation.check_in,
            'number_of_days': reservation.number_of_days,
            'check_out_date': reservation.check_out_date,
            'check_out_time': reservation.check_out_time,
            'status': reservation.status,
            'payment_status': reservation.payment_status,
            'paid_amount': str(reservation.paid_amount),
            'total_price': str(reservation.total_price),
            'price_per_day': str(reservation_room.price_per_day),
            'notes': reservation_room.notes,
        }