# ConnectHub — Modern Social Media Web Application 🌐✨

A complete, fully functional, and visually stunning social networking platform built with **Python Django**, **Vanilla CSS/HTML5/JavaScript**, and **SQLite**. Designed with a professional clean white background and royal blue & purple gradient theme, responsive across mobile, tablet, and desktop devices.

---

## 🌟 Features Overview

### 1. 🏠 Homepage & Dynamic News Feed
- **Personalized Stream:** Logged-in users see posts from creators they follow and their own updates in reverse chronological order.
- **Explore Tab:** Instant toggle to view all public posts across ConnectHub with zero page reloads.
- **Post Composer:** Card with interactive caption box, hashtag highlighting, and live photo upload preview with a 1-click remove option.
- **Creator Highlights & Community Stats:** Real-time statistics showing total posts, registered creators, and community likes.

### 2. 🔐 Authentication & Security
- **Django Built-in Auth:** Complete Registration, Login, and Logout flows with session management.
- **Form Validation:** Enforces alphanumeric handles, unique emails/usernames, minimum password complexity, and live confirmation checks.
- **1-Click Demo Login:** Quick evaluator login buttons for immediate testing (`alex_tech`, `sarah_designs`, `marcus_travels`, `admin`).
- **CSRF & Permissions:** Every form and AJAX request is protected with CSRF tokens. Users can only edit or delete their own posts and comments.

### 3. 👤 User Profiles & Customization
- **Rich Profile Header:** Custom gradient banner, circular profile avatar, full name, `@username`, joined date, location, and clickable portfolio links.
- **Follower Metrics:** Live counts for Followers, Following, Posts, and Total Likes Received.
- **Profile Edit:** Dedicated settings page to update avatar photo with live preview, bio, location, and social links.
- **Interactive Grid & Tabs:** Seamless toggle between "Posts" (3-column photo grid with hover stats) and "Liked Posts".

### 4. 📸 Posts & Comments
- **Media Support:** Upload JPG, PNG, and WebP images up to 5MB with server-side validation.
- **Post Editing & Deletion:** Authors can edit captions, replace photos, or delete posts with instant DOM removal.
- **AJAX Comments:** Comment in real-time without full-page reloads. Comment authors and post authors can delete comments with confirmation.

### 5. ❤️ Like & Unlike System
- **Real-Time AJAX Likes:** Heart icon animates with a bounce effect and updates the like counter instantaneously.
- **Duplicate Prevention:** Database `unique_together` constraint guarantees no duplicate likes from the same user.
- **Full State Sync:** Re-rendering maintains liked state across pages and profiles.

### 6. 🤝 Follow & Unfollow System
- **AJAX Follow Toggle:** Follow or unfollow creators directly from post headers, profile pages, or the "Who to Follow" sidebar widget.
- **Self-Follow Protection:** Backend prevents users from following their own accounts.
- **Smart Feed Filtering:** Feed displays only followed content, automatically suggesting creators if the feed is new.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Python 3.10+, Django 5/6 |
| **Database** | SQLite3 |
| **Frontend** | Semantic HTML5, Vanilla Modern CSS3, Vanilla ES6 JavaScript |
| **Image Processing** | Pillow 10+ |
| **Typography & Icons** | Plus Jakarta Sans & Inter (Google Fonts), Feather-style SVG icons |

---

## ⚡ Quick Start & Installation

### 1. Clone or Open the Project
```bash
cd SocialMediaPlatform
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
> *The seeder automatically generates 5 diverse creators, realistic avatars, follower relationships, and 8+ sample visual posts with comments and likes.*

### 4. Start the Development Server
```bash
python manage.py runserver
```
Visit **`http://127.0.0.1:8000/`** in your browser.

---

## 👥 Demo Evaluator Accounts

All demo accounts share the password: **`password123`** (or use the **1-Click Demo Login** chips on the login page):

| Username | Name | Domain / Role | Password |
| :--- | :--- | :--- | :--- |
| **`alex_tech`** | Alex Rivera | AI Systems Engineer | `password123` |
| **`sarah_designs`** | Sarah Chen | Lead UI/UX Product Designer | `password123` |
| **`marcus_travels`** | Marcus Vance | Travel Photographer | `password123` |
| **`emma_chef`** | Emma Watson | Artisan Baker & Foodie | `password123` |
| **`david_fitness`** | David Miller | Marathon Runner & Coach | `password123` |
| **`admin`** | ConnectHub Admin | Platform Superuser | `admin123` |

---

## 🧪 Automated Testing & Verification

ConnectHub comes with two comprehensive test suites:

### 1. Automated Integration Verification Suite
Runs through all 11 core system requirements end-to-end:
```bash
python verify_social_platform.py
```
**Output:** `SUMMARY: 11/11 INTEGRATION TESTS PASSED (100% SUCCESS)`

### 2. Standard Django Test Suite
```bash
python manage.py test
```
**Output:** `Ran 4 tests in 6.094s — OK`

---

## 📂 Project Directory Structure

```text
SocialMediaPlatform/
├── connecthub_project/        # Project Settings & URL Configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── core/                      # Main Social Media Application
│   ├── models.py              # UserProfile, Post, Comment, Like, Follow
│   ├── views.py               # Feed, Auth, Profile, Post & Comment Views
│   ├── forms.py               # Registration, Login, Post & Profile Forms
│   ├── urls.py                # Application URL routing
│   ├── admin.py               # Django Admin customization
│   ├── tests.py               # Unit & integration tests
│   └── management/
│       └── commands/
│           └── seed_social_data.py # Sample database seeder
├── templates/                 # Modular Semantic HTML Templates
│   ├── base.html              # Base shell with navbar, modals, and footer
│   └── core/
│       ├── home.html          # News feed with composer & sidebars
│       ├── explore.html       # Discovery feed with hashtags & search
│       ├── login.html         # Login with 1-click demo logins
│       ├── register.html      # Sign-up page with profile bio/photo
│       ├── profile.html       # Profile view with stats & photo grid
│       ├── profile_edit.html  # Profile settings & avatar update
│       ├── post_detail.html   # Standalone post with comments
│       ├── post_edit.html     # Edit post caption and photo
│       └── components/        # Reusable template components
├── static/
│   ├── css/
│   │   └── main.css           # Modern design system & styles
│   └── js/
│       └── main.js            # AJAX likes, comments, follows, previews
├── media/                     # User uploaded photos & avatars
├── manage.py
├── requirements.txt
├── verify_social_platform.py  # 11-point automated verification script
└── README.md
```

---

## 📄 License & Attribution
Developed by **Reshmaa Shri E** for the **CodeAlpha Virtual Internship Program**.
