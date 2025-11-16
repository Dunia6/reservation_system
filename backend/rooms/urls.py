from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'rooms', views.RoomViewSet, basename='room')
router.register(r'room-types', views.RoomTypeViewSet, basename='room-type')
router.register(r'floors', views.FloorViewSet, basename='floor')

urlpatterns = [
    path('', include(router.urls)),
]