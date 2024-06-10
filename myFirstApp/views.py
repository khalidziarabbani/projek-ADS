from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from .models import Profile, Category, Product, Expedition, Payment_method, Order, OrderItem, Wishlist

def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        "categories": categories,
        "products": products,
    }
    return render(request, 'index.html', context)

def loginview(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
    elif request.method == 'GET':
        return render(request, 'login.html')

def logoutview(request):
    logout(request)
    return redirect('index')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        full_name = request.POST['full_name']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already in use')
            return render(request, 'register.html')

        # Periksa apakah pengguna sudah memiliki profil
        user = User.objects.create_user(username=username, email=email, password=password)
        if not Profile.objects.filter(user=user).exists():
            Profile.objects.create(user=user, phone_number=phone_number, full_name=full_name)
        else:
            messages.error(request, 'Profile already exists for this user')

        login(request, user)
        messages.success(request, 'Registration successful. You are now logged in.')
        return redirect('login')

    elif request.method == 'GET':
        return render(request, 'register.html')


def product_detail(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        quantity = int(request.POST.get('quantity', 1))
        
        # Check if an order item with the same product and order already exists
        order_item = OrderItem.objects.filter(order=order, product=product).first()
        if order_item:
            # Order item already exists, update the quantity
            order_item.quantity += quantity
            order_item.save()
        else:
            # Create a new order item
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
            )

        return redirect('cart')
    
    elif request.method == 'GET':
        product = get_object_or_404(Product, id=product_id)
        other_products = Product.objects.exclude(id=product_id).order_by('?')[:10]

        context = {
            'product': product,
            'other_products': other_products,
        }
        return render(request, 'product_detail.html', context)


def user(request):
    return render(request, 'user.html')

def categoryPage(request, category_id):
    category = Category.objects.get(id=category_id)
    categories = Category.objects.all()
    products = Product.objects.filter(category=category)
    context = {
        "category": category,
        "categories": categories,
        "products": products,
        }
    return render(request, 'category.html', context)

def delivery(request):
    return render(request, 'delivery.html')


@login_required
def cart(request):
    user = request.user
    # Ensure only one active (incomplete) order per user
    orders = Order.objects.filter(user=user, complete=False)
    if orders.exists():
        if orders.count() > 1:
            # Handle multiple incomplete orders: keep the most recent and mark others as complete or merge them
            main_order = orders.order_by('-date_ordered').first()
            for order in orders.exclude(id=main_order.id):
                # Optionally merge items or just mark them complete
                order.complete = True
                order.save()
        else:
            main_order = orders.first()
    else:
        main_order = Order.objects.create(user=user, complete=False)

    items = main_order.orderitem_set.all()
    subtotal = main_order.get_total_cost

    # Get product IDs in the current order
    product_ids_in_cart = items.values_list('product_id', flat=True)

    # Get products not in the current order
    other_products = Product.objects.exclude(id__in=product_ids_in_cart)

    # Randomly select 10 products from the available products not in the cart
    other_products = random.sample(list(other_products), min(len(other_products), 10))

    context = {
        "items": items,
        "subtotal": subtotal,
        "order": main_order,
        "other_products": other_products,
    }
    return render(request, 'cart.html', context)

@login_required(login_url='login')
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        user = request.user
        order = Order.objects.get_or_create(user=user, complete=False)
        quantity = int(request.POST['quantity', 1])
        
                # Check if an order item with the same product and order already exists
        order_item = OrderItem.objects.filter(order=order, product=product).first()
        if order_item:
            # Order item already exists, update the quantity
            order_item.quantity += quantity
            order_item.save()
        else:
            # Create a new order item
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
            )

        return redirect('cart')
    elif request.method == 'GET':
        product = Product.objects.get(id=product_id)
        context = {
            "product": product,
        }
        return render(request, 'cart.html', context)

def updateItem(request):
    data = json.loads(request.body)
    itemId = data['productId']
    action = data['action']
    
    user = request.user
    orderItem = OrderItem.objects.get(id=itemId)
    product = orderItem.product
    order, created = Order.objects.get_or_create(user=user, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
        orderItem.save()
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        orderItem.save()  
    elif action == 'delete':
        orderItem.delete()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)

@login_required(login_url='login')
def add_to_wishlist(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)

        if product in wishlist.products.all():
            wishlist.products.remove(product)
            messages.error(request, 'Product removed from wishlist.')
        else:
            wishlist.products.add(product)
            messages.success(request, 'Product added to wishlist.')

    return redirect('user')
