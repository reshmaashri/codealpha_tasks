# CodeAlpha Full Stack Web Development Internship Tasks 🚀

Welcome to the official task repository for the **CodeAlpha Virtual Internship Program** in **Full Stack Web Development**.

---

## 👨‍💻 Intern Profile
- **Name:** Reshmaa Shri E
- **Student ID:** `CA/DF1/360477`
- **Domain:** Full Stack Web Development
- **Internship Period:** November 1, 2026 – November 30, 2026
- **GitHub Profile:** [@reshmaashri](https://github.com/reshmaashri)

---

## 📋 Internship Tasks Overview

| Task # | Project Title | Description | Tech Stack | Status |
| :---: | :--- | :--- | :--- | :---: |
| **Task 1** | **[ShopEase — E-Commerce Website](./Task-1_Ecommerce_Store)** | Full-featured, modern e-commerce web app with product catalog, search & filtering, real-time cart management, user authentication, and simulated checkout. | Python Django, SQLite, HTML5, CSS3, JavaScript | **Completed** ✅ |
| **Task 2** | **Social Media Platform / Mini-Feed** | Lightweight social networking app featuring user profiles, dynamic post creation, real-time feed, comments, and likes. | Full-Stack Web Technologies | *In Progress* 🔄 |
| **Task 3** | **Project Management / Kanban Tool** | Team collaboration board with drag-and-drop task workflow, deadlines, priority tags, and status tracking. | Full-Stack Web Technologies | *Planned* ⏳ |

---

## 🌟 Featured Project — Task 1: ShopEase E-Commerce Store

**Folder Location:** [`./Task-1_Ecommerce_Store`](./Task-1_Ecommerce_Store)

### Key Highlights:
1. **Homepage & Navigation**:
   - Modern electric gradient hero banner with featured device showcases.
   - Value propositions bar (Free shipping over $50, 30-day returns, 24/7 customer support).
   - Category cards with live item counts and modern vector icons.
   - Featured products and new arrivals showcase.
2. **Product Listings & Catalog**:
   - Responsive multi-column grid with smooth hover elevations.
   - Category filtering (*Electronics, Wearables, Footwear, Bags & Luggage, Accessories*).
   - Live search querying titles, descriptions, and categories.
   - Multi-option sorting (Newest, Price: Low to High, Price: High to Low, Highest Rated, Name A-Z).
3. **Product Details Page**:
   - High-resolution SVG product illustrations.
   - Star rating, review count, and real-time inventory stock indicators.
   - Interactive quantity stepper (`+` and `−`).
   - AJAX Add to Cart button with animated toast notifications and navbar badge updates.
4. **Shopping Cart Management**:
   - Itemized cart table with product thumbnails and unit prices.
   - Real-time quantity adjustment and item removal.
   - Automatic calculation of Subtotal, Estimated Tax (5%), and Shipping (Free over $50, else $9.99).
   - Promo coupon code system (`WELCOME10`).
5. **User Authentication**:
   - Django built-in User authentication (Sign Up & Login) with input validation.
   - 1-Click Demo Account filler buttons for instant evaluator testing (`customer` / `password123` and `admin` / `admin123`).
   - Protected checkout requiring authentication.
6. **Order Processing & Simulated Checkout**:
   - Full delivery address form.
   - Interactive 3D credit card preview with live typing updates.
   - Simulated payment methods (Credit Card, PayPal, Cash on Delivery).
   - Order Confirmation receipt page with unique Order Number (*e.g. `SE-AB4D1305`*) and `window.print()` receipt layout.
   - Customer Order History (`/orders/`) with status badges.

---

## 🚀 How to Run Task 1 (ShopEase) Locally

### 1. Clone the Repository
```bash
git clone https://github.com/reshmaashri/codealpha_tasks.git
cd codealpha_tasks/Task-1_Ecommerce_Store
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Migrations & Seed Sample Data
```bash
python manage.py migrate
python manage.py seed_data
```
> *This automatically populates 10 realistic products across 5 categories, plus demo customer and admin accounts.*

### 4. Start the Django Server
```bash
python manage.py runserver
```
Visit **`http://127.0.0.1:8000/`** in your browser.

---

## 🧪 Automated Verification Suite
Task 1 includes an automated 15-point integration test script:
```bash
python verify_store.py
```
**Results:** `ALL 15 INTEGRATION TESTS PASSED WITH 100% SUCCESS!`

---

## 📄 License & Attribution
Submitted as part of the **CodeAlpha Virtual Internship Program**. Developed by **Reshmaa Shri E**.
