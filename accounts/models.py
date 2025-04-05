from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Store Manager'),
        ('cashier', 'Cashier'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cashier')

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # Avoids conflict with auth.User
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # Avoids conflict with auth.User
        blank=True
    )

    def __str__(self):
        return f"{self.username} - {self.role}"
