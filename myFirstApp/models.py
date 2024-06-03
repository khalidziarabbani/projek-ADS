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
    stock = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class Expedition(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a expedition (e.g. JNE, TIKI, etc.)', null=True, blank=True)
    image = models.ImageField(upload_to='images/expedition/', null=True, blank=True)
    price = models.FloatField(default=0, null=True, blank=True)
    time_expedition = models.CharField(max_length=200, help_text='Enter time expedition (e.g. 1-2 days, 2-3 days, etc.)', null=True, blank=True)
    def __str__(self):
        return self.name

class Payment_method(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    tax = models.FloatField(default=0, null=True, blank=True)
    image = models.ImageField(upload_to='images/payment_method/', null=True, blank=True)
    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True, blank=True)
    order_number = models.CharField(max_length=10, unique=True, null=True, default=None)
    total_cost = models.FloatField(default=0, null=True, blank=True)
    virtual_account = models.CharField(max_length=12, null=True, blank=True)
    delivery_address = models.TextField(max_length=1000, help_text='Enter delivery address', null=True, blank=True)
    expedition = models.ForeignKey(Expedition, on_delete=models.CASCADE, null=True, blank=True)
    payment_method = models.ForeignKey(Payment_method, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username + ' - ' + self.product.name
    
    @property
    def get_total_cost(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity * item.product.price for item in orderitems])
        return total
    
    @property
    def get_total_quantity(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.product.name + ' - ' + self.order.user.username
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total