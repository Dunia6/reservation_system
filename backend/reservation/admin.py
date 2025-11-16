from django.contrib import admin
from .models import Guest, Reservation, ReservationRoom, Payment


class ReservationRoomInline(admin.TabularInline):
    model = ReservationRoom
    extra = 1
    readonly_fields = ('price_per_day',)


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ('created_by', 'created_at',)
    fields = ('amount', 'payment_method', 'payment_date', 'reference_number', 'notes', 'created_by', 'created_at')


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'id_number', 'type_of_id', 'contact_number', 'email')
    search_fields = ('name', 'id_number', 'contact_number')
    list_filter = ('type_of_id',)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'guest', 'check_in', 'check_out_date', 
        'status', 'payment_status', 'total_price', 'paid_amount', 'get_created_by_info'
    )
    list_filter = ('status', 'payment_status', 'check_in', 'created_by')
    search_fields = ('guest__name', 'guest__id_number', 'created_by__username')
    readonly_fields = ('check_out_date', 'check_out_time', 'total_price', 'created_by', 'get_created_by_full_info', 'created_at', 'updated_at')
    inlines = [ReservationRoomInline, PaymentInline]
    
    def get_created_by_info(self, obj):
        """Display created_by username in list view"""
        if obj.created_by:
            return f"{obj.created_by.username}"
        return "N/A"
    get_created_by_info.short_description = "Créé par"
    
    def get_created_by_full_info(self, obj):
        """Display created_by username and role in detail view"""
        if obj.created_by:
            role = obj.created_by.profile.role if hasattr(obj.created_by, 'profile') else 'N/A'
            return f"{obj.created_by.username} ({role})"
        return "N/A"
    get_created_by_full_info.short_description = "Créé par (utilisateur + rôle)"
    
    fieldsets = (
        ('Guest Information', {
            'fields': ('guest',)
        }),
        ('Reservation Details', {
            'fields': (
                'people_count', 'keys_count', 'check_in', 'number_of_days',
                'check_out_date', 'check_out_time'
            )
        }),
        ('Status', {
            'fields': ('status', 'payment_status')
        }),
        ('Payment', {
            'fields': ('paid_amount', 'total_price')
        }),
        ('Traceability', {
            'fields': ('get_created_by_full_info',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ReservationRoom)
class ReservationRoomAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'room', 'price_per_day')
    list_filter = ('room__floor', 'room__type')
    search_fields = ('reservation__guest__name', 'room__number')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'reservation', 'amount', 'payment_method', 'payment_date', 'get_created_by_info', 'created_at')
    list_filter = ('payment_method', 'payment_date', 'created_by')
    search_fields = ('reservation__id', 'reservation__guest__name', 'reference_number', 'created_by__username')
    readonly_fields = ('created_by', 'get_created_by_full_info', 'created_at',)
    
    def get_created_by_info(self, obj):
        """Display created_by username in list view"""
        if obj.created_by:
            return f"{obj.created_by.username}"
        return "N/A"
    get_created_by_info.short_description = "Créé par"
    
    def get_created_by_full_info(self, obj):
        """Display created_by username and role in detail view"""
        if obj.created_by:
            role = obj.created_by.profile.role if hasattr(obj.created_by, 'profile') else 'N/A'
            return f"{obj.created_by.username} ({role})"
        return "N/A"
    get_created_by_full_info.short_description = "Créé par (utilisateur + rôle)"
    
    fieldsets = (
        ('Reservation', {
            'fields': ('reservation',)
        }),
        ('Payment Details', {
            'fields': ('amount', 'payment_method', 'payment_date', 'reference_number')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Traceability', {
            'fields': ('get_created_by_full_info',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
