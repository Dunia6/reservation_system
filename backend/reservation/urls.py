from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservationViewSet, GuestViewSet


router = DefaultRouter()
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'guests', GuestViewSet, basename='guest')


urlpatterns = [
    path('', include(router.urls)),
]
