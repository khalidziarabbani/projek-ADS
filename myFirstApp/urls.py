from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.loginview, name='login'),
    path('logout/', views.logoutview, name='logout'),
    path('product_detail/', views.product_detail, name='product_detail'),
    path('homepage/', views.homepage, name='homepage'),
    path('user/', views.user, name='user'),
]
