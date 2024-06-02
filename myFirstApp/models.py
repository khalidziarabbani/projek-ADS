from django.db import models
from django.contrib.auth.models import User
import random

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)  # Menambahkan default
    phone_number = models.CharField(max_length=15, default='-')
    full_name = models.CharField(max_length=255, default='Anonymous')
    address = models.TextField(max_length=1000, help_text='Enter address of the user', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/category/', null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    detail_name= models.TextField(max_length=1000, help_text='Enter Detail name of the product', null=True, blank=True)
    price = models.FloatField(default=0)
    year_released = models.IntegerField(default=random.randint(2000, 2024))
    description = models.TextField(max_length=1000, help_text='Enter description of the product', null=True, blank=True)
    brand = models.CharField(max_length=200, help_text='Enter brand of the product', null=True, blank=True)
    condition = models.CharField(max_length=200, help_text='Enter condition of the product', null=True, blank=True)
    image = models.ImageField(upload_to='images/product/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name