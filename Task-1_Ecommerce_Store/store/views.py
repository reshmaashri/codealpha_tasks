import json
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .forms import UserRegistrationForm, UserLoginForm, CheckoutForm
from .cart_utils import get_or_create_cart


def home_view(request):
    """
    Homepage displaying modern hero banner, featured products, categories,
    and value propositions.
    """
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_featured=True)[:6]
    new_arrivals = Product.objects.all().order_by('-created_at')[:8]

    context = {
        'categories': categories,
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
    }
    return render(request, 'store/home.html', context)


def product_list_view(request):
    """
    Product listing page with full category filter, search query,
    sorting, and price range.
    """
    products = Product.objects.all()
    categories = Category.objects.all()

    # Category filter
    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    # Search filter
    search_query = request.GET.get('q', '').strip()
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    # Stock filter
    in_stock_only = request.GET.get('in_stock')
    if in_stock_only == '1':
        products = products.filter(stock__gt=0)

    # Price range filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=Decimal(min_price))
        except Exception:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=Decimal(max_price))
        except Exception:
            pass

    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
        'sort_by': sort_by,
        'min_price': min_price or '',
        'max_price': max_price or '',
        'in_stock_only': in_stock_only == '1',
        'total_count': products.count(),
    }
    return render(request, 'store/product_list.html', context)


def product_detail_view(request, slug):
    """
    Product details page displaying full images, pricing, availability,
    specs, and related products.
    """
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


def cart_view(request):
    """
    Shopping cart page showing items, quantities, subtotal, tax,
    free shipping calculation, and checkout trigger.
    """
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()

    subtotal = cart.total_price
    # Free shipping on orders over $50, otherwise $9.99
    if subtotal > Decimal('50.00') or subtotal == Decimal('0.00'):
        shipping = Decimal('0.00')
    else:
        shipping = Decimal('9.99')

    # Estimated 5% sales tax
    tax = round(subtotal * Decimal('0.05'), 2)
    grand_total = subtotal + shipping + tax

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)


def add_to_cart_view(request, product_id):
    """
    Add a product to cart with chosen quantity.
    Supports regular form submission and AJAX fetch requests.
    """
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)

    quantity = 1
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            quantity = 1

    if quantity < 1:
        quantity = 1

    if product.stock < quantity:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax') == '1':
            return JsonResponse({
                'success': False,
                'message': f'Sorry, only {product.stock} items currently in stock!'
            }, status=400)
        messages.error(request, f'Sorry, only {product.stock} items in stock!')
        return redirect(request.META.get('HTTP_REFERER', 'product_list'))

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        if cart_item.quantity + quantity > product.stock:
            cart_item.quantity = product.stock
            messages.warning(request, f'Quantity adjusted to available stock ({product.stock}).')
        else:
            cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    success_msg = f'"{product.name}" was added to your cart!'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax') == '1':
        return JsonResponse({
            'success': True,
            'message': success_msg,
            'cart_item_count': cart.total_items,
            'cart_total': str(cart.total_price),
        })

    messages.success(request, success_msg)
    return redirect(request.META.get('HTTP_REFERER', 'cart'))


def update_cart_item_view(request, item_id):
    """
    Update item quantity in cart (+ or - or direct input).
    """
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            if cart_item.quantity < cart_item.product.stock:
                cart_item.quantity += 1
                cart_item.save()
            else:
                messages.warning(request, f'Cannot exceed available stock of {cart_item.product.stock}.')
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
                messages.info(request, f'"{cart_item.product.name}" removed from cart.')
                return redirect('cart')
        elif action == 'set':
            try:
                new_qty = int(request.POST.get('quantity', 1))
                if new_qty > 0:
                    cart_item.quantity = min(new_qty, cart_item.product.stock)
                    cart_item.save()
                else:
                    cart_item.delete()
                    return redirect('cart')
            except (ValueError, TypeError):
                pass

    return redirect('cart')


def remove_from_cart_view(request, item_id):
    """
    Remove an item completely from the cart.
    """
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()

    messages.info(request, f'"{product_name}" was removed from your cart.')
    return redirect('cart')


@login_required(login_url='login')
def checkout_view(request):
    """
    Checkout page protected by authentication.
    Processes shipping info, validates order, creates simulated order,
    updates inventory, and redirects to confirmation.
    """
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()

    if not cart_items.exists():
        messages.warning(request, "Your shopping cart is empty. Please add items before checking out.")
        return redirect('product_list')

    subtotal = cart.total_price
    shipping = Decimal('0.00') if subtotal > Decimal('50.00') else Decimal('9.99')
    tax = round(subtotal * Decimal('0.05'), 2)
    grand_total = subtotal + shipping + tax

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.shipping_cost = shipping
            order.total_amount = grand_total
            order.status = 'Processing'
            order.payment_status = 'Paid (Simulated)'
            order.save()

            # Create OrderItems and decrement stock
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    price=item.product.final_price,
                    quantity=item.quantity
                )
                # Decrement stock
                if item.product.stock >= item.quantity:
                    item.product.stock -= item.quantity
                else:
                    item.product.stock = 0
                item.product.save()

            # Clear the cart items
            cart.items.all().delete()

            messages.success(request, f"Order #{order.order_number} placed successfully! Thank you for shopping with ShopEase.")
            return redirect('order_confirmation', order_number=order.order_number)
        else:
            messages.error(request, "Please check the form for any missing or invalid fields.")
    else:
        # Pre-fill form if user has name/email
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
        }
        form = CheckoutForm(initial=initial_data)

    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)


def order_confirmation_view(request, order_number):
    """
    Order receipt confirmation page displaying order details,
    simulated transaction ID, and full itemized summary.
    """
    order = get_object_or_404(Order, order_number=order_number)

    # If order is linked to a user, make sure only the owner (or staff) can view it if logged in
    if order.user and request.user.is_authenticated and order.user != request.user and not request.user.is_staff:
        messages.error(request, "You are not authorized to view this order confirmation.")
        return redirect('home')

    order_items = order.items.all()

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'store/order_confirmation.html', context)


@login_required(login_url='login')
def my_orders_view(request):
    """
    View user's order history.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'store/my_orders.html', context)


def register_view(request):
    """
    User registration view. Automatically logs in the user on successful signup.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            old_session_key = request.session.session_key
            login(request, user)

            # Migrate guest cart items to user cart
            if old_session_key:
                guest_cart = Cart.objects.filter(session_key=old_session_key, user=None).first()
                if guest_cart:
                    user_cart, _ = Cart.objects.get_or_create(user=user)
                    for item in guest_cart.items.all():
                        existing = CartItem.objects.filter(cart=user_cart, product=item.product).first()
                        if existing:
                            existing.quantity += item.quantity
                            existing.save()
                        else:
                            item.cart = user_cart
                            item.save()
                    guest_cart.delete()

            messages.success(request, f"Welcome to ShopEase, {user.username}! Your account has been created.")

            next_url = request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            messages.error(request, "Registration could not be completed. Please review errors below.")
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'store/register.html', context)


def login_view(request):
    """
    User login view with friendly error notifications and redirect handling.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                old_session_key = request.session.session_key
                login(request, user)

                # Migrate guest cart items to user cart
                if old_session_key:
                    guest_cart = Cart.objects.filter(session_key=old_session_key, user=None).first()
                    if guest_cart:
                        user_cart, _ = Cart.objects.get_or_create(user=user)
                        for item in guest_cart.items.all():
                            existing = CartItem.objects.filter(cart=user_cart, product=item.product).first()
                            if existing:
                                existing.quantity += item.quantity
                                existing.save()
                            else:
                                item.cart = user_cart
                                item.save()
                        guest_cart.delete()

                messages.success(request, f"Welcome back, {user.username}!")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = UserLoginForm()


    next_param = request.GET.get('next', '')
    context = {
        'form': form,
        'next': next_param,
    }
    return render(request, 'store/login.html', context)


def logout_view(request):
    """
    Log out the user and display a farewell notification.
    """
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.info(request, f"You have been successfully logged out, {username}. Come back soon!")
    return redirect('home')
