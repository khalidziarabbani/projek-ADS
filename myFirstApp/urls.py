from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.loginview, name='login'),
    path('logout/', views.logoutview, name='logout'),
    path('user/', views.user, name='user'),
    path('edit_image/', views.edit_image, name='edit_image'),
    path('change_password/', views.change_password, name='change_password'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', views.categoryPage, name='category'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('updateItem/', views.updateItem, name='updateItem'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('payment/', views.payment, name='payment'),
    path('transaction_list/', views.transaction_list, name='transaction_list'),
    path('success_state/', views.success_state, name='success_state'),
]
