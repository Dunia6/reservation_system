from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CompanyInformation
from .serializers import CompanyInformationSerializer
from core.permissions import IsManager, IsSuperviseur, IsManagerOrSuperviseur


class CompanyInformationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing company information"""
    queryset = CompanyInformation.objects.all()
    serializer_class = CompanyInformationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """Lecture pour tous, modification pour Manager et Superviseur"""
        if self.action in ['list', 'retrieve', 'current']:
            return [IsAuthenticated()]
        return [IsManagerOrSuperviseur()]
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current company information (first record)"""
        company = CompanyInformation.objects.first()
        if company:
            serializer = self.get_serializer(company)
            return Response(serializer.data)
        return Response(
            {"message": "Aucune information d'entreprise configurée"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    @action(detail=False, methods=['post', 'put'])
    def update_current(self, request):
        """Update or create company information"""
        company = CompanyInformation.objects.first()
        
        if company:
            serializer = self.get_serializer(company, data=request.data, partial=True)
        else:
            serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
