from django.db import models

# Create your models here.

class Floor(models.Model):
    """ Model representing a floor in the hotel. """
    number = models.IntegerField(unique=True)

    def __str__(self):
        return f"Floor {self.number}"


class RoomType(models.Model):
    """ Model representing a type of hotel room. """
    name = models.CharField(max_length=50, unique=True)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class Room(models.Model):
    """ Model representing a hotel room. """
    STATUS_CHOICES = [
        ('available', 'Disponible'),
        ('occupied', 'Occupée'),
        ('maintenance', 'En maintenance'),
    ]
    
    number = models.CharField(max_length=10, unique=True)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"Room {self.number} - {self.type}"
