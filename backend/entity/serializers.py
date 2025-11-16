from rest_framework import serializers
from .models import CompanyInformation


class CompanyInformationSerializer(serializers.ModelSerializer):
    """Serializer for Company Information model"""
    currency_display = serializers.CharField(source='get_currency_display', read_only=True)
    
    class Meta:
        model = CompanyInformation
        fields = [
            'id', 'name', 'city', 'commune', 'avenue', 
            'quarter', 'phone', 'email', 'currency', 'currency_display'
        ]
        read_only_fields = ['id', 'currency_display']
