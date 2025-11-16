# Django imports
from django.contrib.auth import authenticate
from django.conf import settings
from django.db import transaction

# DRF imports
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

# JWT imports
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

# Swagger/OpenAPI imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Local imports
from .serializers import LoginSerializer, UserDetailSerializer
from .utils import set_refresh_cookie, delete_refresh_cookie
from .models import Profile, User

# Create your views here.



class UserViewSet(viewsets.GenericViewSet):
    """ ViewSet for managing users. """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def get_serializer_class(self):
        if self.action == 'me':
            return UserDetailSerializer
        return LoginSerializer
    
    
    def get_permissions(self):
        if self.action in ['me']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


    @swagger_auto_schema(
        operation_description="Connexion utilisateur avec email et mot de passe",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                'Connexion réussie',
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='JWT Access Token')
                    }
                )
            ),
            400: 'Données de connexion invalides',
            401: 'Identifiants incorrects'
        },
        tags=['Authentication']
    )
    @action(detail=False, methods=['post'])
    def login(self, request) -> Response:
        """ Handle user login. """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "errors": "Données de connexion invalides !"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(
            username=serializer.validated_data['username'], 
            password=serializer.validated_data['password']
        )

        if user is None:
            return Response(
                {
                    "errors": "Données de connexion invalides !"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        
        response = Response(
            {
                "access": str(access),
                "user": UserDetailSerializer(user).data
            },
            status=status.HTTP_200_OK
        )
        
        set_refresh_cookie(response, str(refresh))

        return response


    @swagger_auto_schema(
        operation_description="Déconnexion utilisateur et révocation du refresh token",
        responses={
            200: 'Déconnexion réussie',
            400: 'Aucun token trouvé ou token invalide'
        },
        tags=['Authentication']
    )
    @action(detail=False, methods=['post'])
    def logout(self, request) -> Response:
        """ Handle user logout. """
        refresh_token = request.COOKIES.get(settings.REFRESH_TOKEN_COOKIE_NAME)

        if not refresh_token:
            return Response(
                {
                    "errors": "Aucun jeton de rafraîchissement trouvé dans les cookies !"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            response = Response({"detail": "Déconnexion réussie."}, status=status.HTTP_200_OK)
            delete_refresh_cookie(response)
            
            return response
            
        except TokenError:
            return Response(
                {"detail": "Token invalide ou expiré."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    

    @swagger_auto_schema(
        operation_description="Rafraîchir le access token avec le refresh token",
        responses={
            200: openapi.Response(
                'Token rafraîchi avec succès',
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='Nouveau JWT Access Token')
                    }
                )
            ),
            400: 'Token invalide ou expiré'
        },
        tags=['Authentication']
    )
    @action(detail=False, methods=['post'])
    def refresh(self, request) -> Response:
        """ Handle token refresh. """
        
        refresh_token = request.COOKIES.get(settings.REFRESH_TOKEN_COOKIE_NAME)

        if not refresh_token:
            return Response(
                {
                    "errors": "Aucun jeton de rafraîchissement trouvé dans les cookies !"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            new_access = token.access_token

            response = Response(
                {
                    "access": str(new_access)
                },
                status=status.HTTP_200_OK
            )

            return response

        except TokenError:
            return Response(
                {"detail": "Token invalide ou expiré."},
                status=status.HTTP_400_BAD_REQUEST
            )
    

    @swagger_auto_schema(
        operation_description="Récupérer les informations de l'utilisateur connecté",
        responses={
            200: openapi.Response('Détails de l\'utilisateur', UserDetailSerializer),
            401: 'Utilisateur non authentifié'
        },
        tags=['User']
    )
    @action(detail=False, methods=['get'])
    def me(self, request) -> Response:
        """ Retrieve details of the authenticated user. """
        user = request.user

        if not user.is_authenticated:
            return Response(
                {
                    "errors": "Utilisateur non authentifié."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer(user)

        print(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)