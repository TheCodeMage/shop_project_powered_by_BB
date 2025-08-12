# shop/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, Category, CartItem


# -------------------------------
# Home Page
# -------------------------------
def home(request):
    return render(request, 'home.html')


# -------------------------------
# Shop Page - Show products and categories
# -------------------------------
def shop(request):
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category__id=category_id)
    else:
        products = Product.objects.all()

    categories = Category.objects.all()
    return render(request, 'shop.html', {
        'products': products,
        'categories': categories
    })


# -------------------------------
# Product Detail Page
# -------------------------------
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


# -------------------------------
# Add to Cart
# -------------------------------
@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    cart_item.quantity += 1
    cart_item.save()
    return redirect('shop')


# -------------------------------
# Remove from Cart
# -------------------------------
@login_required
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart_item = CartItem.objects.get(user=request.user, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('shop')


# -------------------------------
# View Cart
# -------------------------------
@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# -------------------------------
# Update Cart Item Quantity
# -------------------------------
@login_required
def update_quantity(request, item_id):
    if request.method == 'POST':
        try:
            cart_item = CartItem.objects.get(id=item_id, user=request.user)
            action = request.POST.get('action')
            
            if action == 'increase':
                cart_item.quantity += 1
                cart_item.save()
            elif action == 'decrease':
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()
                    return JsonResponse({'removed': True})
            
            # Calculate new total
            cart_items = CartItem.objects.filter(user=request.user)
            new_total = sum(item.total_price() for item in cart_items)
            
            return JsonResponse({
                'success': True,
                'new_quantity': cart_item.quantity if cart_item.quantity > 0 else 0,
                'new_total': cart_item.total_price() if cart_item.quantity > 0 else 0,
                'cart_total': new_total
            })
            
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


# -------------------------------
# Remove Item from Cart
# -------------------------------
@login_required
def remove_item(request, item_id):
    if request.method == 'POST':
        try:
            cart_item = CartItem.objects.get(id=item_id, user=request.user)
            cart_item.delete()
            
            # Calculate new total
            cart_items = CartItem.objects.filter(user=request.user)
            new_total = sum(item.total_price() for item in cart_items)
            
            return JsonResponse({
                'success': True,
                'cart_total': new_total
            })
            
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


# -------------------------------
# Signup
# -------------------------------
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST.get('role', 'user')  # 'admin' or 'user'

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password)
        
        if role == 'admin':
            user.is_staff = True  # can access admin panel
        user.save()

        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')

    return render(request, 'auth/signup.html')


# -------------------------------
# Login
# -------------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'auth/login.html')


# -------------------------------
# Logout
# -------------------------------
def logout_view(request):
    logout(request)
    return redirect('home')
