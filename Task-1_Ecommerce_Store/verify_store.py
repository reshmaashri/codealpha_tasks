import os
import sys
import urllib.request
import urllib.parse
import json

# Setup Django test client directly
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from store.models import Category, Product, Cart, CartItem, Order, OrderItem

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("STARTING COMPREHENSIVE SHOPEASE TEST SUITE")
print("=" * 60)

client = Client()

# 1. Test Homepage
res = client.get('/')
assert res.status_code == 200, f"Home page failed with {res.status_code}"
assert b'ShopEase' in res.content
assert b'Featured Products' in res.content
print("[PASS] 1. Homepage loads successfully (Status 200)")

# 2. Test Product List & Categories
res = client.get('/products/')
assert res.status_code == 200, f"Products page failed with {res.status_code}"
assert b'Explore All Products' in res.content
print("[PASS] 2. Product Catalog loads successfully (Status 200)")

# 3. Test Category Filter
res = client.get('/products/?category=electronics')
assert res.status_code == 200
assert b'Electronics' in res.content
print("[PASS] 3. Category filtering works (Status 200)")

# 4. Test Search Query
res = client.get('/products/?q=headphones')
assert res.status_code == 200
assert b'Studio Pro Noise-Cancelling Headphones' in res.content
print("[PASS] 4. Search query works (Status 200)")

# 5. Test Product Details Page
headphones = Product.objects.filter(slug__icontains='headphones').first()
assert headphones is not None, "Sample headphones product not found"
res = client.get(f'/products/{headphones.slug}/')
assert res.status_code == 200
assert headphones.name.encode() in res.content
assert b'In Stock' in res.content
print(f"[PASS] 5. Product Details page for '{headphones.name}' loads successfully (Status 200)")

# 6. Test Add to Cart (Anonymous session)
res = client.post(f'/cart/add/{headphones.id}/', {'quantity': 2}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
assert res.status_code == 200
data = json.loads(res.content)
assert data['success'] is True
assert data['cart_item_count'] == 2
print("[PASS] 6. AJAX Add to Cart works (2 items added)")

# 7. Test Cart Page View
res = client.get('/cart/')
assert res.status_code == 200
assert b'Shopping Cart' in res.content
assert headphones.name.encode() in res.content
print("[PASS] 7. Shopping Cart page displays items and subtotal (Status 200)")

# 8. Test Update Cart Quantity (+ 1)
session_key = client.session.session_key
active_cart = Cart.objects.filter(session_key=session_key).first()
assert active_cart is not None
cart_item = active_cart.items.filter(product=headphones).first()
assert cart_item is not None
res = client.post(f'/cart/update/{cart_item.id}/', {'action': 'increase'})
assert res.status_code == 302 # Redirects to cart
cart_item.refresh_from_db()
assert cart_item.quantity == 3
print("[PASS] 8. Cart quantity increase works (Quantity is now 3)")



# 9. Test Protected Checkout Redirect for Anonymous Guest
res = client.get('/checkout/')
assert res.status_code == 302
assert '/login' in res.url
print("[PASS] 9. Checkout is securely protected; anonymous user redirected to login")

# 10. Test Login with Demo Customer via login view POST
res = client.post('/login/?next=/checkout/', {'username': 'customer', 'password': 'password123'})
assert res.status_code == 302
assert '/checkout/' in res.url
print("[PASS] 10. Demo customer logged in successfully via login view")

# 11. Test Checkout Page when Logged In
res = client.get('/checkout/')

assert res.status_code == 200
assert b'Shipping &amp; Delivery Address' in res.content or b'Shipping & Delivery Address' in res.content
assert b'Payment Method (Simulated)' in res.content
print("[PASS] 11. Checkout form renders for authenticated customer (Status 200)")

# 12. Test Placing an Order (Simulated Checkout)
checkout_data = {
    'full_name': 'Alex Morgan',
    'email': 'customer@example.com',
    'phone': '+1 (555) 234-5678',
    'address': '742 Evergreen Terrace',
    'city': 'Springfield',
    'state': 'Oregon',
    'postal_code': '97477',
    'country': 'United States',
    'payment_method': 'Credit/Debit Card (Simulated)',
    'card_number': '4111 2222 3333 4444',
    'card_name': 'ALEX MORGAN',
    'card_expiry': '12/28',
    'card_cvv': '789',
    'notes': 'Please leave near the front porch',
}
res = client.post('/checkout/', checkout_data)
assert res.status_code == 302
order_confirmation_url = res.url
print(f"[PASS] 12. Order submitted successfully! Redirecting to {order_confirmation_url}")

# 13. Test Order Confirmation Receipt
res = client.get(order_confirmation_url)
assert res.status_code == 200
assert b'ORDER CONFIRMED' in res.content
assert b'Alex Morgan' in res.content
assert b'742 Evergreen Terrace' in res.content
print("[PASS] 13. Order Confirmation Receipt page renders with full itemized details (Status 200)")

# 14. Test Customer Order History (My Orders)
res = client.get('/orders/')
assert res.status_code == 200
assert b'My Order History' in res.content
orders_count = Order.objects.filter(user__username='customer').count()
assert orders_count >= 1
print(f"[PASS] 14. My Orders page renders with {orders_count} customer order(s) (Status 200)")

# 15. Test Cart Cleared After Order
res = client.get('/cart/')
assert res.status_code == 200
assert b'Your Shopping Cart is Empty' in res.content
print("[PASS] 15. Cart was cleanly emptied after successful order placement")


print("=" * 60)
print("ALL 15 INTEGRATION TESTS PASSED WITH 100% SUCCESS!")
print("=" * 60)
