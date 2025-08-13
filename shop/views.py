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

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    # ✅ Success notification
    messages.success(request, f"{product.name} has been added to your cart!")  # ✅ Show notification
    
    # Redirect back to where the request came from
    referer = request.META.get('HTTP_REFERER', None)
    if referer:
        return redirect(referer)
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
# Update Cart Item Quantity (Fixed to allow quantity=0)
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
                message = "Quantity updated"
            elif action == 'decrease':
                cart_item.quantity -= 1
                if cart_item.quantity <= 0:
                    cart_item.delete()
                    return JsonResponse({
                        'success': True, 
                        'removed': True, 
                        'message': 'Item removed from cart'
                    })
                else:
                    cart_item.save()
                    message = "Quantity updated"
            elif action == 'set':
                # Allow setting specific quantity including 0
                new_quantity = int(request.POST.get('quantity', 1))
                if new_quantity <= 0:
                    cart_item.delete()
                    return JsonResponse({
                        'success': True, 
                        'removed': True, 
                        'message': 'Item removed from cart'
                    })
                else:
                    cart_item.quantity = new_quantity
                    cart_item.save()
                    message = "Quantity updated"
            
            # Calculate new total
            cart_items = CartItem.objects.filter(user=request.user)
            new_total = sum(item.total_price() for item in cart_items)
            
            return JsonResponse({
                'success': True,
                'new_quantity': cart_item.quantity if cart_item.quantity > 0 else 0,
                'new_total': cart_item.total_price() if cart_item.quantity > 0 else 0,
                'cart_total': new_total,
                'message': message
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
# Checkout - Clear cart and return success
# -------------------------------
@login_required
def checkout(request):
    if request.method == 'POST':
        try:
            # Get all cart items for the user
            cart_items = CartItem.objects.filter(user=request.user)
            cart_count = cart_items.count()
            
            if cart_count == 0:
                return JsonResponse({
                    'success': False,
                    'message': 'Your cart is empty'
                })
            
            # Calculate total
            total = sum(item.total_price() for item in cart_items)
            
            # Clear the cart
            cart_items.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Checkout successful! Cart cleared.',
                'total': total
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Checkout failed: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


# -------------------------------  
# Add to Cart with Quantity (Enhanced)
# -------------------------------
@login_required
def add_to_cart_with_quantity(request, product_id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id)
            quantity = int(request.POST.get('quantity', 1))
            
            if quantity <= 0:
                return JsonResponse({
                    'success': False,
                    'message': 'Quantity must be greater than 0'
                })
            
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user, 
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            # Get updated cart count
            cart_count = CartItem.objects.filter(user=request.user).count()
            
            return JsonResponse({
                'success': True,
                'message': 'Item added to cart',
                'cart_count': cart_count
            })
            
        except Product.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Product not found'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


# -------------------------------  
# Get Cart Count (for navbar)
# -------------------------------
@login_required
def get_cart_count(request):
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0
    
    return JsonResponse({'cart_count': cart_count})


# -------------------------------  
# Logout
# -------------------------------
def logout_view(request):
    logout(request)
    return redirect('home')
