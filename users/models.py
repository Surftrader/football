from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Field username, email, date_joined are inherited from AbstractUser
    email = models.EmailField(unique=True)
    
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='manager')
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    