from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Profile(models.Model):
    """ Profile Model """

    ROLE_CHOICES = (
        ('Receptionniste', 'Receptionniste'),
        ('Manager', 'Manager'),
        ('Superviseur', 'Superviseur'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='unknown')

    def __str__(self):
        return f"{self.user.username} - {self.role}"