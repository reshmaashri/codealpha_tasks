import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.conf import settings
from core.models import UserProfile, Post, Comment, Like, Follow


def create_aesthetic_image(width, height, title, subtitle, tag, color1, color2, style="tech"):
    """
    Generates a high-resolution, beautiful social media post image with
    smooth gradients, geometric patterns, and typography.
    """
    img = Image.new('RGB', (width, height), color=color1)
    draw = ImageDraw.Draw(img)

    # Draw smooth vertical/diagonal gradient
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    for y in range(height):
        factor = y / height
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Add decorative geometric shapes/glows based on style
    if style == "tech":
        # Tech grid and subtle circular overlays
        for x in range(0, width, 60):
            draw.line([(x, 0), (x, height)], fill=(255, 255, 255, 25), width=1)
        for y in range(0, height, 60):
            draw.line([(0, y), (width, y)], fill=(255, 255, 255, 25), width=1)
        # Circles
        draw.ellipse([width - 320, -80, width + 120, 360], outline=(255, 255, 255, 40), width=3)
        draw.ellipse([width - 240, 0, width + 40, 280], outline=(255, 255, 255, 60), width=2)
    elif style == "nature":
        # Mountain peaks or waves
        points = [
            (0, height),
            (0, height - 260),
            (width * 0.28, height - 420),
            (width * 0.55, height - 280),
            (width * 0.82, height - 460),
            (width, height - 320),
            (width, height)
        ]
        draw.polygon(points, fill=(255, 255, 255, 30))
        # Sun / Moon
        draw.ellipse([width - 220, 80, width - 80, 220], fill=(255, 240, 200, 180))
    elif style == "design":
        # Modern glassmorphic cards and floating bubbles
        draw.rounded_rectangle([60, 60, width - 60, height - 180], radius=32, outline=(255, 255, 255, 70), width=3)
        draw.rounded_rectangle([100, 100, width - 100, height - 220], radius=24, outline=(255, 255, 255, 45), width=2)
    else:
        # Radial vibe
        draw.ellipse([-100, height - 300, 400, height + 200], outline=(255, 255, 255, 45), width=4)
        draw.ellipse([width - 200, -100, width + 200, 300], outline=(255, 255, 255, 45), width=4)

    # Fallback to default font
    try:
        font_large = ImageFont.truetype("arial.ttf", 46)
        font_medium = ImageFont.truetype("arial.ttf", 26)
        font_tag = ImageFont.truetype("arial.ttf", 20)
    except Exception:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_tag = ImageFont.load_default()

    # Draw Tag pill
    draw.rounded_rectangle([70, 70, 70 + len(tag) * 14 + 40, 115], radius=16, fill=(0, 0, 0, 70))
    draw.text((88, 80), tag.upper(), fill=(255, 255, 255), font=font_tag)

    # Title & Subtitle
    draw.text((70, height - 160), title, fill=(255, 255, 255), font=font_large)
    draw.text((72, height - 95), subtitle, fill=(230, 235, 245), font=font_medium)

    buf = BytesIO()
    img.save(buf, format='JPEG', quality=92)
    return ContentFile(buf.getvalue())


def create_avatar_image(name, initials, color1, color2):
    """Creates a colorful circular avatar image."""
    img = Image.new('RGB', (200, 200), color=color1)
    draw = ImageDraw.Draw(img)

    r1, g1, b1 = color1
    r2, g2, b2 = color2
    for y in range(200):
        factor = y / 200
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        draw.line([(0, y), (200, y)], fill=(r, g, b))

    try:
        font = ImageFont.truetype("arial.ttf", 64)
    except Exception:
        font = ImageFont.load_default()

    draw.text((62, 60), initials, fill=(255, 255, 255), font=font)

    buf = BytesIO()
    img.save(buf, format='PNG')
    return ContentFile(buf.getvalue())


class Command(BaseCommand):
    help = "Seeds sample realistic creators, posts, comments, likes, and followers for ConnectHub"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting ConnectHub seed process..."))

        # 1. Create Admin Superuser
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@connecthub.io",
                "first_name": "ConnectHub",
                "last_name": "Admin",
                "is_staff": True,
                "is_superuser": True,
            }
        )
        admin_user.set_password("admin123")
        admin_user.save()
        admin_profile, _ = UserProfile.objects.get_or_create(user=admin_user)
        admin_profile.bio = "Official ConnectHub Platform Administrator. Keeping the feed vibrant and secure! 🛡️✨"
        admin_profile.location = "San Francisco, CA"
        admin_profile.website = "https://connecthub.io"
        admin_profile.save()

        # 2. Creators Profile Data
        creators_data = [
            {
                "username": "alex_tech",
                "password": "password123",
                "first_name": "Alex",
                "last_name": "Rivera",
                "email": "alex.rivera@techpulse.dev",
                "bio": "AI Systems Engineer & Open Source Contributor. Building scalable neural pipelines and sharing developer insights. 🚀💻",
                "location": "Seattle, WA",
                "website": "https://alexrivera.dev",
                "c1": (37, 99, 235),
                "c2": (79, 70, 229),
                "initials": "AR"
            },
            {
                "username": "sarah_designs",
                "password": "password123",
                "first_name": "Sarah",
                "last_name": "Chen",
                "email": "sarah@chenstudio.design",
                "bio": "Lead Product Designer & Minimalist. Obsessed with clean typography, micro-interactions, and accessible digital spaces. 🎨✨",
                "location": "New York, NY",
                "website": "https://sarahchendesign.com",
                "c1": (124, 58, 237),
                "c2": (236, 72, 153),
                "initials": "SC"
            },
            {
                "username": "marcus_travels",
                "password": "password123",
                "first_name": "Marcus",
                "last_name": "Vance",
                "email": "marcus@vanceexpeditions.com",
                "bio": "Travel Photographer & Visual Storyteller. 42 countries explored and counting. Capturing the raw beauty of earth. 🏔️✈️",
                "location": "Zurich, Switzerland",
                "website": "https://vancegallery.photo",
                "c1": (5, 150, 105),
                "c2": (6, 182, 212),
                "initials": "MV"
            },
            {
                "username": "emma_chef",
                "password": "password123",
                "first_name": "Emma",
                "last_name": "Watson",
                "email": "emma@thegoldenloaf.kitchen",
                "bio": "Artisan Baker, Recipe Creator & Food Stylist. Turning flour and sourdough starters into edible poetry. 🥖🥐",
                "location": "Paris, France",
                "website": "https://thegoldenloaf.kitchen",
                "c1": (217, 119, 6),
                "c2": (245, 158, 11),
                "initials": "EW"
            },
            {
                "username": "david_fitness",
                "password": "password123",
                "first_name": "David",
                "last_name": "Miller",
                "email": "david@athleticflow.co",
                "bio": "Marathon Runner & Strength Coach. Dedicated to helping creators maintain peak mental and physical energy. 🏃‍♂️⚡️",
                "location": "Austin, TX",
                "website": "https://athleticflow.co",
                "c1": (220, 38, 38),
                "c2": (244, 63, 94),
                "initials": "DM"
            },
        ]

        created_users = [admin_user]

        for udata in creators_data:
            user, _ = User.objects.get_or_create(
                username=udata["username"],
                defaults={
                    "first_name": udata["first_name"],
                    "last_name": udata["last_name"],
                    "email": udata["email"],
                }
            )
            user.set_password(udata["password"])
            user.save()

            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.bio = udata["bio"]
            profile.location = udata["location"]
            profile.website = udata["website"]

            # Save avatar image
            if not profile.avatar:
                avatar_file = create_avatar_image(udata["first_name"], udata["initials"], udata["c1"], udata["c2"])
                profile.avatar.save(f"{udata['username']}_avatar.png", avatar_file, save=False)
            profile.save()

            created_users.append(user)
            self.stdout.write(f"  Created user: @{user.username}")

        # 3. Follow Network
        follow_pairs = [
            ("alex_tech", "sarah_designs"),
            ("alex_tech", "marcus_travels"),
            ("sarah_designs", "alex_tech"),
            ("sarah_designs", "marcus_travels"),
            ("sarah_designs", "emma_chef"),
            ("marcus_travels", "alex_tech"),
            ("marcus_travels", "sarah_designs"),
            ("marcus_travels", "david_fitness"),
            ("emma_chef", "sarah_designs"),
            ("emma_chef", "alex_tech"),
            ("david_fitness", "marcus_travels"),
            ("david_fitness", "alex_tech"),
            ("admin", "alex_tech"),
            ("admin", "sarah_designs"),
        ]

        for follower_uname, following_uname in follow_pairs:
            f_user = User.objects.filter(username=follower_uname).first()
            t_user = User.objects.filter(username=following_uname).first()
            if f_user and t_user and f_user != t_user:
                Follow.objects.get_or_create(follower=f_user, following=t_user)

        self.stdout.write("  Setup follower relationships.")

        # 4. Posts Data
        posts_spec = [
            {
                "author": "alex_tech",
                "title": "Edge Neural Engine 2.0",
                "subtitle": "40% latency reduction achieved on mobile silicon",
                "tag": "Artificial Intelligence",
                "style": "tech",
                "c1": (30, 41, 59),
                "c2": (79, 70, 229),
                "caption": "Just benchmarked our latest on-device quantized model! 🚀 Over 40% latency reduction without any noticeable perplexity degradation. Edge AI is truly arriving faster than expected. What is your go-to optimization framework this year? #technology #ai #engineering #coding #innovation",
                "comments": [
                    ("sarah_designs", "This is huge for UX latency! Instant UI responses make all the difference. 🔥"),
                    ("marcus_travels", "Can't wait to test this inside photo post-processing pipelines on mobile!"),
                    ("david_fitness", "Incredible progress Alex, keep crushing it!")
                ]
            },
            {
                "author": "sarah_designs",
                "title": "Minimalist Design Systems",
                "subtitle": "Tokenized colors, responsive rhythm & accessibility",
                "tag": "Design & UI/UX",
                "style": "design",
                "c1": (79, 70, 229),
                "c2": (192, 38, 211),
                "caption": "Good design is as little design as possible. ✨ Spent the week refactoring our core design system tokens. Consistent spatial rhythm and WCAG AAA color contrast ratios bring immense joy to my workflow. How do you approach cross-platform tokens? #design #ui #ux #minimalism #webdesign",
                "comments": [
                    ("alex_tech", "Clean tokens make frontend developer handoffs 10x faster! Love this palette."),
                    ("emma_chef", "The color harmony here is so calming and crisp. Beautiful work Sarah! 💜")
                ]
            },
            {
                "author": "marcus_travels",
                "title": "Alpine Sunrise Panorama",
                "subtitle": "Elevation 3,200m in the heart of Zermatt, Switzerland",
                "tag": "Photography & Nature",
                "style": "nature",
                "c1": (15, 23, 42),
                "c2": (5, 150, 105),
                "caption": "Hiked up at 4:30 AM with 18kg of camera gear to witness this golden crown touching the Matterhorn peaks. The cold was biting, but stillness like this recharges the soul. 🏔️🌅 #travel #photography #nature #mountains #wanderlust",
                "comments": [
                    ("david_fitness", "That altitude climb is no joke with 18kg on your back! Respect Marcus! 👊"),
                    ("sarah_designs", "That lighting is pure cinema. Absolutely breathtaking framing.")
                ]
            },
            {
                "author": "emma_chef",
                "title": "Wild Yeast Sourdough Boule",
                "subtitle": "78% hydration, 36-hour cold ferment & blistered crust",
                "tag": "Artisan Baking",
                "style": "food",
                "c1": (180, 83, 9),
                "c2": (245, 158, 11),
                "caption": "There is something truly meditative about the rhythm of stretch-and-folds. Fresh out of the oven: a 36-hour cold fermented sourdough boule with an open, airy crumb and signature ear blister. 🥖✨ Who wants a slice with salted cultured butter? #baking #foodie #artisan #sourdough #homemade",
                "comments": [
                    ("alex_tech", "That blistered crust is perfection! Shipping me a loaf to Seattle? 😄"),
                    ("marcus_travels", "Nothing beats fresh bread after a long trek. Looks delicious Emma!")
                ]
            },
            {
                "author": "david_fitness",
                "title": "Morning 10K Bridge Tempo",
                "subtitle": "Pacing 4:15/km under the Texas sunrise",
                "tag": "Health & Endurance",
                "style": "fitness",
                "c1": (185, 28, 28),
                "c2": (239, 68, 68),
                "caption": "Early mornings are when champions are built. 10k tempo run locked in before the city woke up. Remember: consistency beats intensity every single day of the week. Lace up and move! 🏃‍♂️⚡️ #fitness #running #marathon #discipline #health",
                "comments": [
                    ("sarah_designs", "4:15/km pace is flying! Great reminder to get my morning workout in."),
                    ("alex_tech", "Cardio clarity is real. Good run David!")
                ]
            },
            {
                "author": "alex_tech",
                "title": "Next-Gen Developer Workstations",
                "subtitle": "Ultrawide setups, mechanical keys & Linux kernels",
                "tag": "Dev Setup",
                "style": "tech",
                "c1": (30, 58, 138),
                "c2": (99, 102, 241),
                "caption": "Rebuilt my desk workstation with cable concealment, 144Hz curved ultrawide, and a customized split mechanical keyboard. Workspace ergonomics pay massive compound dividends on code quality. 🖥️⌨️ #workspace #coding #developer #setup #tech",
                "comments": [
                    ("sarah_designs", "Clean cable management is peak engineering satisfaction."),
                    ("david_fitness", "Ergonomics matter big time. Good posture keeps energy high.")
                ]
            },
            {
                "author": "sarah_designs",
                "title": "Glassmorphism in Modern UI",
                "subtitle": "Balancing backdrop blur with tactile physical realism",
                "tag": "Product Design",
                "style": "design",
                "c1": (109, 40, 217),
                "c2": (14, 165, 233),
                "caption": "Exploring subtle depth layers using backdrop-filter blur and micro-specular highlights. The goal is tactile physical presence without cluttering user focus. 📱🎨 #ui #ux #design #productdesign #creativity",
                "comments": [
                    ("alex_tech", "Looks crisp! Modern CSS backdrop-filter is finally rock solid across browsers.")
                ]
            },
            {
                "author": "marcus_travels",
                "title": "Kyoto Bamboo Groves at Dawn",
                "subtitle": "Silent whispers of the Arashiyama forest path",
                "tag": "Japan Chronicles",
                "style": "nature",
                "c1": (4, 120, 87),
                "c2": (16, 185, 129),
                "caption": "Walking alone through the Arashiyama bamboo path before the crowds arrive. The soft clicking sound of giant bamboo swaying in the morning breeze is an experience I will never forget. 🎋🇯🇵 #japan #kyoto #travel #photography #zen",
                "comments": [
                    ("emma_chef", "Kyoto is magical! Did you stop by Nishiki market for morning matcha?"),
                    ("marcus_travels", "Yes! The matcha pastries were incredible Emma!")
                ]
            }
        ]

        # Clean existing posts if needed or add new
        post_count = 0
        for spec in posts_spec:
            author = User.objects.filter(username=spec["author"]).first()
            if not author:
                continue

            img_file = create_aesthetic_image(
                width=1080,
                height=1080,
                title=spec["title"],
                subtitle=spec["subtitle"],
                tag=spec["tag"],
                color1=spec["c1"],
                color2=spec["c2"],
                style=spec["style"]
            )

            post = Post(author=author, caption=spec["caption"])
            post.image.save(f"seed_post_{spec['author']}_{post_count}.jpg", img_file, save=True)
            post_count += 1

            # Add Likes
            for liker in created_users:
                if liker != author:
                    Like.objects.get_or_create(post=post, user=liker)

            # Add Comments
            for c_author_uname, c_text in spec["comments"]:
                c_user = User.objects.filter(username=c_author_uname).first()
                if c_user:
                    Comment.objects.create(post=post, author=c_user, text=c_text)

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {post_count} posts with comments, likes, and followers!"))
        self.stdout.write(self.style.SUCCESS("ConnectHub is ready for testing!"))
