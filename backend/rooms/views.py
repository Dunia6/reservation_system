from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import Room, RoomType, Floor
from .serializers import RoomSerializer, RoomDetailSerializer, RoomTypeSerializer, FloorSerializer
from core.permissions import IsManager, IsSuperviseur, IsManagerOrSuperviseur

# Create your views here.


class RoomViewSet(viewsets.ModelViewSet):
    """ ViewSet for managing rooms. """
    queryset = Room.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """Receptionniste: lecture seule et patch, Manager et Superviseur: toutes opérations"""
        if self.action in ['list', 'retrieve', 'occupancy_stats', 'partial_update']:
            return [IsAuthenticated()]
        return [IsManagerOrSuperviseur()]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RoomDetailSerializer
        return RoomSerializer

    @action(detail=False, methods=['get'], url_path='occupancy-stats')
    def occupancy_stats(self, request):
        """Get room occupancy statistics by floor"""
        floors = Floor.objects.all().order_by('number')
        
        stats_by_floor = []
        total_rooms = 0
        total_occupied = 0
        total_available = 0
        total_maintenance = 0
        
        for floor in floors:
            rooms = Room.objects.filter(floor=floor)
            
            occupied_count = rooms.filter(status='occupied').count()
            available_count = rooms.filter(status='available').count()
            maintenance_count = rooms.filter(status='maintenance').count()
            total_count = rooms.count()
            
            total_rooms += total_count
            total_occupied += occupied_count
            total_available += available_count
            total_maintenance += maintenance_count
            
            stats_by_floor.append({
                'floor_number': floor.number,
                'floor_name': f'Niveau {floor.number}',
                'total_rooms': total_count,
                'occupied': occupied_count,
                'available': available_count,
                'maintenance': maintenance_count
            })
        
        return Response({
            'by_floor': stats_by_floor,
            'summary': {
                'total_rooms': total_rooms,
                'occupied': total_occupied,
                'available': total_available,
                'maintenance': total_maintenance
            }
        }, status=status.HTTP_200_OK)


class RoomTypeViewSet(viewsets.ModelViewSet):
    """ ViewSet for managing room types. """
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', ]
    
    def get_permissions(self):
        """Manager et Superviseur peuvent créer/modifier, tous peuvent lire"""
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsManagerOrSuperviseur()]


class FloorViewSet(viewsets.ModelViewSet):
    """ ViewSet for managing floors. """
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', ]
    
    def get_permissions(self):
        """Manager et Superviseur peuvent créer/modifier, tous peuvent lire"""
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsManagerOrSuperviseur()]