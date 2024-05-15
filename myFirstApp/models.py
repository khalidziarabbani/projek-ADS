from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)  # Menambahkan default
    phone_number = models.CharField(max_length=15, default='-')
    full_name = models.CharField(max_length=255, default='Anonymous')

    def __str__(self):
        return self.user.username