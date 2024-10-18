
from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    # Extend the default User model with additional fields
    age = models.PositiveIntegerField(null=True, blank=True)
    interests = models.TextField(null=True, blank=True)
    financial_goals = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username
