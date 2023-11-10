from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from .models import Cart, Product, CartItem, Order, OrderItem

from .forms import ProductForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
            # Redirect to a success page.
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')
            # Return an 'invalid login' error message.
    return render(request, 'login.html')

# Implement similar views for logout and registration.
def logout_view(request):
    logout(request)
    return redirect('index')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            cart = Cart(user=user)
            cart.save()
            # Log the user in after registration, if needed.
            # Redirect to a success page or any desired URL after successful registration.
            return redirect('login')  # Assuming 'login' is the name of your login URL.
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def view_cart(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    products = Product.objects.all()
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart.html', {'cart': cart, 'cart_items': cart_items, 'products': products})

def add_to_cart(request, product_id):
    user = request.user
    cart = Cart.objects.get(user=user)
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('index')

def sub_from_cart(request, product_id):
    user = request.user
    cart = Cart.objects.get(user=user)
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()
    return redirect('view_cart')

def delete_from_cart(request, product_id):
    user = request.user
    cart = Cart.objects.get(user=user)
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.delete()
    else:
        cart_item.save()
    
    return redirect('view_cart')

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(user=request.user)
            # Additional logic if needed
            return redirect('index')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


def view_product(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product.html', {'product': product})

def view_my_product(request):
    user = request.user
    products = Product.objects.filter(user=user)
    return render(request, 'my_products.html', {'products': products})

def delete_my_product(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    
    product.delete()
    return redirect('view_my_product')

def buy_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = product.user
    
    # Create an order for the user if it doesn't exist
    order, created = Order.objects.get_or_create(user=user)

    # Add the product to the order
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    order_item.quantity += 1
    order_item.complete = False
    order_item.save()

    return redirect('index')

def view_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    return render(request, 'orders.html', {'orders': orders})

def save_to_orders(request):
    user = request.user
    cart = user.cart
    cart_items = cart.cartitem_set.all()

    # Add cart items to the order
    for cart_item in cart_items:
        order, created = Order.objects.get_or_create(user=cart_item.product.user)

        order_item, created = OrderItem.objects.get_or_create(order=order, product=cart_item.product)
        order_item.quantity += cart_item.quantity
        order_item.complete = False
        order_item.save()

    # Clear the user's cart after saving to orders
    cart_items.delete()

    return redirect('view_cart')  # Redirect to the view orders page

def complete_orders(request, order_id):
    order_item = get_object_or_404(OrderItem, id=order_id)

    order_item.delete()

    return redirect('view_orders')
