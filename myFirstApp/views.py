from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django import forms
import random
from django.http import JsonResponse
from django.http import HttpResponseBadRequest  # Import added
import json
from django.db import transaction

from .models import Profile, Category, Product, Expedition, Payment_method, Order, OrderItem, Wishlist, Shipment

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
        product = Product.objects.get(id=product_id)
        other_products = Product.objects.exclude(id=product_id).order_by('?')[:10]

        context = {
            'product': product,
            'other_products': other_products,
        }
        return render(request, 'product_detail.html', context)

@login_required(login_url='login')
def user(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST['username']
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        profile = Profile.objects.get(user=user)
        user.username = username
        profile.full_name = full_name
        user.email = email
        profile.address = address
        profile.phone_number = phone_number
        user.save()
        profile.save()
        return redirect('user')
    elif request.method == 'GET':
        user = request.user
        try:
            wishlist = Wishlist.objects.get(user=user)
        except Wishlist.DoesNotExist:
            wishlist = None
        context = {
            "wishlist": wishlist.products.all() if wishlist else [],
        }
        return render(request, 'user.html', context)

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

@login_required
def cart(request):
    user = request.user
    # Ensure only one active (incomplete) order per user
    orders = Order.objects.filter(user=user, complete=False)
    if orders.exists():
        if orders.count() > 1:
            main_order = orders.order_by('-date_ordered').first()
            for order in orders.exclude(id=main_order.id):
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
        order, created = Order.objects.get_or_create(user=user, complete=False)
        quantity = int(request.POST.get('quantity', 1))
        
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        order_item.quantity += quantity
        order_item.save()

        return redirect('cart')
    elif request.method == 'GET':
        product = get_object_or_404(Product, id=product_id)
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

    if action == 'add' and orderItem.quantity < product.stock:
        orderItem.quantity = (orderItem.quantity + 1)
        orderItem.save()
    elif action == 'remove' and orderItem.quantity > 0:
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

def edit_image(request):
    if request.method == 'POST':
        if 'profile_image' in request.FILES:
            try:
                profile = Profile.objects.get(user=request.user)
                profile.image = request.FILES['profile_image']
                profile.save()
                return redirect('user')
            except Profile.DoesNotExist:
                pass

    return render(request, 'user.html')

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            user = request.user
            if user.check_password(old_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Password changed successfully')
                    return redirect('user')
                else:
                    messages.error(request, 'New passwords do not match')
            else:
                messages.error(request, 'Invalid old password')
        else:
            messages.error(request, 'Invalid form submission')
    else:
        form = ChangePasswordForm()
    return render(request, 'user.html', {'form': form})

def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('index')
    return render(request, 'user.html')

# @login_required(login_url='login')
# def payment(request):
#     user = request.user

#     # Handle GET request to display payment page
#     if request.method == 'GET':
#         expeditions = Expedition.objects.all()
#         payment_methods = Payment_method.objects.all()
        
#         # Get or create order for the current user
#         order, created = Order.objects.get_or_create(user=user, complete=False)
#         order_items = order.orderitem_set.all()

#         # Generate order number and virtual account if it's a new order
#         if created:
#             order.date_ordered = timezone.now()
#             order_number = order.generate_random_number(length=5)
#             virtual_account = order.generate_random_number(length=12)
#             order.order_number = order_number
#             order.virtual_account = virtual_account
#             order.save()

#         # Redirect to cart if there are no items in the order
#         if not order_items:
#             return redirect('cart')

#         # Calculate subtotal for the order
#         subtotal = order.get_total_cost
#         total_payment = order.get_total_payment

#         context = {
#             "order": order,
#             "order_items": order_items,
#             "subtotal": subtotal,
#             "total_payment": total_payment,
#             "expeditions": expeditions,
#             "payment_methods": payment_methods,
#             "virtual_account": order.virtual_account,
#             "order_number": order.order_number,
#         }

#         return render(request, 'payment.html', context)

#     # Handle POST request for processing payment
#     elif request.method == 'POST':
#         try:
#             # Extract data from POST request
#             delivery_address = request.POST.get('delivery_address')
#             total_payment = float(request.POST.get('total_payment').replace('$', ''))
#             expedition_id = int(request.POST.get('expedition'))
#             payment_method_id = int(request.POST.get('payment_method'))

#             # Retrieve expedition and payment method objects
#             expedition = get_object_or_404(Expedition, id=expedition_id)
#             payment_method = get_object_or_404(Payment_method, id=payment_method_id)

#             # Retrieve or create order for the current user
#             order, created = Order.objects.get_or_create(user=user, complete=False)

#             # Update order details
#             order.delivery_address = delivery_address
#             order.expedition = expedition
#             order.payment_method = payment_method
#             order.total_cost = total_payment
#             order.save()

#             # Create shipment record
#             Shipment.objects.create(
#                 user=user,
#                 order=order,
#                 delivery_address=delivery_address,
#             )

#             # Mark order as complete if specified in POST data
#             if request.POST.get('type') == 'now':
#                 order.complete = True
#                 order.save()

#             # Process each order item (if any)
#             for order_item in order.orderitem_set.all():
#                 product = order_item.product
#                 product.stock -= order_item.quantity
#                 product.save()

#             # Redirect to transaction list or success page
#             return redirect('transaction_list')

#         except ValueError as e:
#             return HttpResponseBadRequest(f"Invalid input: {e}")

#     return HttpResponseBadRequest("Invalid request method")

@login_required(login_url='login')
def payment(request):
    if request.method == 'GET':
        user = request.user
        expeditions = Expedition.objects.all()
        payment_methods = Payment_method.objects.all()
        order, created = Order.objects.get_or_create(user=user, complete=False)
        order_items = order.orderitem_set.all()
        order.date_ordered = timezone.now()
        order_number = random.randint(10000, 99999)
        virtual_account = random.randint(100000000000, 999999999999)
        order.order_number = order_number
        order.virtual_account = virtual_account
        order.save()
        
        if not order_items:
            return redirect('cart')

        subtotal = order.get_total_cost
        total_payment = order.get_total_payment
        context = {
            "expeditions": expeditions,
            "payment_methods": payment_methods,
            "order_items": order_items,
            "subtotal": subtotal,
            "order": order,
            "order_number": order_number,
            "virtual_account": virtual_account,
            "total_payment": total_payment,
        }
        return render(request, 'payment.html', context)
    elif request.method == 'POST':
        try:
            user = request.user
            delivery_address = request.POST['delivery_address']
            total_payment = float(request.POST['total_payment'].replace('$', ''))

            expedition_id = request.POST.get('expedition')
            expedition = get_object_or_404(Expedition, price=expedition_id)  # Ganti 'price' dengan field yang sesuai dalam model Expedition
            payment_method_id = request.POST.get('payment_method')
            payment_method = get_object_or_404(Payment_method, tax=payment_method_id)  # Ganti 'tax' dengan field yang sesuai dalam model Payment_method

            order, created = Order.objects.get_or_create(user=user, complete=False)
            order.expedition = expedition
            order.payment_method = payment_method
            order.total_cost = total_payment
            order.delivery_address = delivery_address
            if request.POST['type'] == 'now':
                order.complete = True
            order.save()

            Shipment.objects.create(
                user=user,
                order=order,
                delivery_address=delivery_address,
            )
            
            return redirect('transaction_list')

        except ValueError as e:
            return HttpResponseBadRequest(f"Invalid input: {e}")

@login_required(login_url='login')
def transaction_list(request):
    user = request.user
    if request.method == 'GET':
        orders = Order.objects.filter(user=user, complete=True).order_by('-date_ordered')
        context = {
            "orders": orders,
        }
        return render(request, 'transaction_list.html', context)
