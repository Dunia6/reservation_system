from django.contrib import admin
from .models import Room, Floor, RoomType

# Register your models here.

@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('number',)
    search_fields = ('number',)

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_night')
    search_fields = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'floor', 'type', 'is_available')
    list_filter = ('floor', 'type', 'is_available')
    search_fields = ('number',)
    ordering = ('floor__number', 'number')


