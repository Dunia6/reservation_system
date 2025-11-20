from django.db import models
from django.contrib.auth.models import User
from rooms.models import Room

from datetime import timedelta
from django.db import models

# Create your models here.


class Guest(models.Model):
    SEX_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    type_of_id = models.CharField(max_length=50)
    id_number = models.CharField(max_length=50, unique=True)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS = [
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
    ]

    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='reservations')
    people_count = models.PositiveIntegerField()
    keys_count = models.PositiveIntegerField()


    check_in = models.DateTimeField()
    number_of_days = models.PositiveIntegerField()
    check_out_date = models.DateField(blank=True, null=True)
    check_out_time = models.TimeField(blank=True, null=True)



    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='unpaid')
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.check_out_date:
            self.check_out_date = (self.check_in + timedelta(days=self.number_of_days)).date()
        if not self.check_out_time:
            self.check_out_time = (self.check_in + timedelta(days=self.number_of_days)).time()
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        """Calculate total price from all reservation rooms"""
        total = sum(
            res_room.price_per_day * self.number_of_days 
            for res_room in self.reservation_rooms.all()
        )
        return total

    @property
    def remaining_amount(self):
        """Calculate remaining amount to pay"""
        return self.total_price - self.paid_amount

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reservation {self.id} - {self.guest.name}"


class ReservationRoom(models.Model):
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name='reservation_rooms'
    )
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='reservation_rooms'
    )
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Room {self.room.number} in Reservation {self.reservation.id}"


class Payment(models.Model):
    """Model to track payment history for reservations"""
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Espèces'),
        ('mobile_money', 'Mobile Money'),
        ('bank_transfer', 'Virement Bancaire'),
        ('credit_card', 'Carte de Crédit'),
        ('check', 'Chèque'),
    ]
    
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_date = models.DateTimeField()
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments_created')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Payment {self.id} - {self.amount} FC for Reservation {self.reservation.id}"
