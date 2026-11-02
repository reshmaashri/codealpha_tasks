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
| **Task 2** | **[ConnectHub — Social Media Platform](./Task-2_SocialMediaPlatform)** | Modern, fully functional social networking web app featuring news feed, user profiles, posts with image uploads, real-time AJAX likes, comments, and follow system. | Python Django, SQLite, HTML5, Vanilla CSS3, JavaScript | **Completed** ✅ |
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

### 1. Navigate to Task 1 Folder
```bash
cd Task-1_Ecommerce_Store
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

## 🌟 Featured Project — Task 2: ConnectHub Social Media Platform

**Folder Location:** [`./Task-2_SocialMediaPlatform`](./Task-2_SocialMediaPlatform)

### Key Highlights:
1. **Homepage & News Feed**:
   - 3-column desktop layout (Left navigation & user card, Center dynamic stream, Right widgets).
   - Feed tabs: "Following Feed" (creators you follow + your posts) vs "Explore All" (public community posts).
   - In-feed post composer with live photo upload preview and remove button.
   - Responsive mobile navigation with bottom app bar.
2. **User Authentication & Profiles**:
   - Registration with live input validation, username format checks, bio, and custom profile photo upload.
   - Login supporting username or email, plus **1-Click Demo Accounts** for instant evaluator testing.
   - User profile pages with custom cover banners, avatar, bio, location, website links, joined dates, and live follower/following counts.
   - Profile tabs: 3-column photo grid with hover statistics (likes & comments count) and "Liked Posts".
   - Profile edit page to update avatar, bio, location, and links with instant image preview.
3. **Posts & Comments**:
   - Create posts with high-res photos and rich captions with highlighted `#hashtags`.
   - Edit post captions or replace photos; delete own posts with modal confirmation.
   - Chronological stream ordering.
   - Real-time AJAX comments without page reload, plus comment deletion.
4. **Like & Unlike System**:
   - Instant AJAX toggle with heart bounce keyframe animation.
   - Live counter updates.
   - Database `unique_together` constraint guarantees no duplicate likes from the same user.
5. **Follow & Unfollow System**:
   - Follow and unfollow creators from profile pages, post cards, or the "Who to Follow" sidebar widget.
   - Backend validation prevents users from following themselves.
   - Dynamic follower and following count updates.
6. **Design & Aesthetics**:
   - Clean white background (`#F8FAFC` base, `#FFFFFF` cards) with professional electric blue and purple theme (`#4F46E5`, `#7C3AED`, `#2563EB`).
   - Smooth micro-interactions, modal dialogs, and slide-in toast notifications.

---

## 🚀 How to Run Task 2 (ConnectHub) Locally

### 1. Navigate to Task 2 Folder
```bash
cd Task-2_SocialMediaPlatform
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Migrations & Seed Sample Data
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_social_data
```
> *This automatically populates 5 realistic creators, avatars, follower relationships, and 8+ sample visual posts with comments and likes.*

### 4. Start the Django Server
```bash
python manage.py runserver
```
Visit **`http://127.0.0.1:8000/`** in your browser.

### 5. Demo Accounts for Instant Testing:
All accounts share the password: **`password123`**
- `alex_tech` (AI Systems Engineer)
- `sarah_designs` (Lead UI/UX Designer)
- `marcus_travels` (Travel Photographer)
- `emma_chef` (Artisan Baker)
- `david_fitness` (Fitness Coach)
- `admin` / `admin123` (Platform Superuser)

---

## 🧪 Automated Testing & Verification

Both tasks include comprehensive test suites:

### Task 1 Tests:
```bash
cd Task-1_Ecommerce_Store
python verify_store.py
```
**Results:** `ALL 15 INTEGRATION TESTS PASSED WITH 100% SUCCESS!`

### Task 2 Tests:
```bash
cd Task-2_SocialMediaPlatform
python verify_social_platform.py
python manage.py test
```
**Results:** `11/11 INTEGRATION TESTS PASSED (100% SUCCESS)` and `Ran 4 tests in 6.094s — OK`

---

## 📄 License & Attribution
Submitted as part of the **CodeAlpha Virtual Internship Program**. Developed by **Reshmaa Shri E**.

