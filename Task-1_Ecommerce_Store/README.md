# ShopEase - Modern Beginner-Friendly E-Commerce Website

ShopEase is a full-featured, responsive e-commerce web application built with **Python Django**, **Vanilla HTML5/CSS3/JavaScript**, and **SQLite**. It features a modern, clean design with rich micro-animations, glassmorphism accents, live search, dynamic shopping cart, protected simulated checkout, and order history tracking.

---

## 🌟 Key Features

1. **Modern Homepage**:
   - Electric gradient hero banner with call-to-actions and featured device badge.
   - Value propositions bar (Free shipping over $50, 30-day returns, 24/7 support, secure checkout).
   - Category cards with icons and live product counts.
   - Featured products and new arrivals showcase.
   - VIP club newsletter subscription form with instant feedback.

2. **Product Listings & Catalog (`/products/`)**:
   - Responsive multi-column grid with hover card elevation and smooth image transitions.
   - Category filtering (Electronics, Wearables, Footwear, Bags & Luggage, Accessories).
   - Live search querying titles, descriptions, and categories.
   - Multi-option sorting (Newest, Price: Low to High, Price: High to Low, Highest Rated, Name A-Z).
   - In-stock availability badges and active filters indicator.

3. **Product Details Page (`/products/<slug>/`)**:
   - High-resolution SVG product artwork and specs breakdown.
   - Star rating, review count, and inventory stock indicators.
   - Interactive quantity stepper (+ and − buttons).
   - AJAX-powered Add to Cart button with real-time feedback toast.
   - Related products carousel in the same category.

4. **Shopping Cart (`/cart/`)**:
   - Complete itemized cart list with product thumbnails and unit prices.
   - Increase, decrease, or remove item actions.
   - Dynamic real-time calculation of Subtotal, Estimated Tax (5%), and Shipping (Free over $50, else $9.99).
   - Promo coupon code field (`WELCOME10` support).
   - Empty cart state with quick "Start Shopping" button.

5. **Authentication System**:
   - User Registration (`/register/`) with input validation and password confirmation.
   - User Login (`/login/`) with automatic post-login redirection (e.g., returning to checkout).
   - 1-Click Demo Account filler buttons for instant testing.
   - Django built-in User authentication with session persistence.

6. **Order Processing & Simulated Checkout (`/checkout/`)**:
   - Protected: Only logged-in customers can complete checkout.
   - Delivery address collection (Full Name, Email, Phone, Address, City, State, Postal Code, Country, Delivery Notes).
   - Simulated payment methods:
     - Credit/Debit Card (with live interactive 3D card preview updating as you type).
     - PayPal (Simulated Express).
     - Cash on Delivery.
   - Automatic stock decrement and cart clearing upon successful checkout.
   - Order Confirmation receipt page (`/order-confirmation/<order_number>/`) with printable receipt (`window.print()`).
   - Customer Order History (`/orders/`) displaying past purchases and status pills.

---

## 📁 Project Folder Structure

```text
EcommerceStore/
│
├── manage.py                     # Django CLI management script
├── requirements.txt              # Project dependencies
├── db.sqlite3                    # SQLite database with seed data
├── README.md                     # Documentation & setup guide
│
├── ecommerce_project/            # Project configuration
│   ├── __init__.py
│   ├── settings.py               # Django settings (apps, templates, static)
│   ├── urls.py                   # Master URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── store/                        # Core e-commerce application
│   ├── __init__.py
│   ├── admin.py                  # Django admin registration
│   ├── apps.py                   # App configuration
│   ├── cart_utils.py             # Cart session and user merging logic
│   ├── context_processors.py     # Global cart counter & category injection
│   ├── forms.py                  # Registration, Login, and Checkout forms
│   ├── models.py                 # Category, Product, Cart, CartItem, Order, OrderItem
│   ├── urls.py                   # Store URL endpoints
│   ├── views.py                  # Store controller views
│   ├── migrations/               # Database schema migrations
│   └── management/
│       └── commands/
│           └── seed_data.py      # Automated database seeder script
│
├── static/                       # Static assets
│   ├── css/
│   │   └── style.css             # Vanilla CSS design system & responsive layout
│   ├── js/
│   │   └── main.js               # AJAX cart, quantity stepper, card preview, toasts
│   └── images/
│       └── products/             # High-res SVG product illustrations
│           ├── headphones.svg
│           ├── smartwatch.svg
│           ├── laptop.svg
│           ├── shoes.svg
│           ├── bag.svg
│           ├── backpack.svg
│           ├── keyboard.svg
│           ├── sunglasses.svg
│           ├── sneakers.svg
│           └── waterbottle.svg
│
└── templates/                    # HTML Django templates
    ├── base.html                 # Master layout (navbar, toast system, footer)
    └── store/
        ├── home.html             # Landing homepage
        ├── product_list.html     # Catalog with filters & search
        ├── product_detail.html   # Product details & specs
        ├── cart.html             # Shopping cart
        ├── checkout.html         # Protected simulated checkout
        ├── order_confirmation.html # Receipt and confirmation
        ├── my_orders.html        # User order history
        ├── login.html            # Sign in page
        └── register.html         # Sign up page
```

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
Open your terminal inside the `EcommerceStore` directory and install the requirements:
```bash
pip install -r requirements.txt
```

### 2. Apply Database Migrations
Create the SQLite database tables:
```bash
python manage.py migrate
```

### 3. Seed Sample Data (Products & Demo Accounts)
Populate the database with sample products, categories, and test accounts:
```bash
python manage.py seed_data
```

This creates:
- **10 Sample Products** across 5 categories with pricing, stock, and images.
- **Customer Account**: Username: `customer` | Password: `password123`
- **Admin Superuser**: Username: `admin` | Password: `admin123`

### 4. Run the Development Server
Start the Django server:
```bash
python manage.py runserver
```
Visit **`http://127.0.0.1:8000/`** in your browser to explore the store.

---

## 🧪 Testing Every Feature

1. **Browse Products**:
   - Navigate to `http://127.0.0.1:8000/` to view the homepage.
   - Click "Products" in the top navbar or select any category card to filter items.
   - Use the search bar to query products (e.g., search `headphones` or `shoes`).
   - Test sorting (Price: Low to High, Highest Rated, etc.).

2. **View Product Details**:
   - Click "View Details" on any product card.
   - Change the quantity using the `+` and `−` stepper buttons.
   - Click "Add to Cart". Notice the instant success toast notification and live cart badge counter update in the navbar!

3. **Manage Shopping Cart**:
   - Click the cart icon in the navbar (`/cart/`).
   - Increase or decrease quantities directly using the `+` and `−` buttons.
   - Watch the Subtotal, Shipping, and Total calculate automatically.
   - Remove an item by clicking the trash icon.

4. **User Registration & Login**:
   - Click "Log In" in the navbar.
   - Click the **"👤 Customer Account"** button to 1-click auto-fill (`customer` / `password123`).
   - Click "Sign In". Notice your username appears in the header with a dropdown menu.

5. **Simulated Checkout & Order Processing**:
   - Go to `/cart/` and click "Proceed to Checkout".
   - Notice the pre-filled customer details.
   - Select "Credit / Debit Card (Instant Simulation)" and type a simulated card number to see the live interactive card preview animate.
   - Click "Place Simulated Order".
   - You will be redirected to the **Order Confirmation** page with your unique Order ID (e.g. `SE-A1B2C3D4`), itemized receipt, and printable layout.

6. **Track Orders**:
   - Click your username dropdown in the navbar and select **"My Orders"** (`/orders/`).
   - See your placed order with status `Processing`, total amount, and link to view the receipt.

7. **Django Admin**:
   - Visit `http://127.0.0.1:8000/admin/`.
   - Log in with `admin` / `admin123` to manage categories, products, orders, and users.
