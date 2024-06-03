from django.contrib import admin

from .models import Profile, Category, Product, Expedition, Payment_method, Order, OrderItem
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Expedition)
admin.site.register(Payment_method)
admin.site.register(Order)
admin.site.register(OrderItem)