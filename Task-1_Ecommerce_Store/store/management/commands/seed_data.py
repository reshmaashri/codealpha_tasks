from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Category, Product


class Command(BaseCommand):
    help = 'Seeds database with categories, realistic sample products, and demo accounts.'

    def handle(self, *args, **options):
        self.stdout.write("Seeding ShopEase database...")

        # 1. Create Demo Users
        admin_user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@shopease.com', 'is_staff': True, 'is_superuser': True})
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: admin / admin123"))

        demo_user, created = User.objects.get_or_create(username='customer', defaults={'email': 'customer@example.com', 'first_name': 'Alex', 'last_name': 'Morgan'})
        if created:
            demo_user.set_password('password123')
            demo_user.save()
            self.stdout.write(self.style.SUCCESS("Created demo customer: customer / password123"))

        # 2. Create Categories
        categories_data = [
            {'name': 'Electronics', 'icon': 'bi-laptop', 'description': 'Cutting-edge gadgets, computing, and premium audio equipment.'},
            {'name': 'Wearables', 'icon': 'bi-smartwatch', 'description': 'Smart devices and biometric health tracking watches.'},
            {'name': 'Footwear', 'icon': 'bi-fire', 'description': 'Ergonomic athletic runners, sneakers, and lifestyle footwear.'},
            {'name': 'Bags & Luggage', 'icon': 'bi-bag', 'description': 'Handcrafted leather briefcases and modern commute backpacks.'},
            {'name': 'Accessories', 'icon': 'bi-sunglasses', 'description': 'Everyday carry items, polarized eyewear, and thermal drinkware.'},
        ]

        cat_objs = {}
        for cdata in categories_data:
            cat, _ = Category.objects.get_or_create(
                name=cdata['name'],
                defaults={'icon': cdata['icon'], 'description': cdata['description']}
            )
            cat_objs[cdata['name']] = cat

        # 3. Create Sample Products
        products_data = [
            {
                'name': 'Studio Pro Noise-Cancelling Headphones',
                'category': 'Electronics',
                'description': 'Engineered with active hybrid noise cancellation, 40mm custom drivers, and up to 45 hours of battery life. Includes plush memory foam ear cushions, crystal-clear voice microphones, and instant Bluetooth 5.3 multipoint pairing.',
                'price': Decimal('249.99'),
                'discount_price': Decimal('199.99'),
                'image_url': '/static/images/products/headphones.svg',
                'stock': 24,
                'is_featured': True,
                'rating': Decimal('4.9'),
                'review_count': 128,
            },
            {
                'name': 'Apex Horizon Smartwatch Series 7',
                'category': 'Wearables',
                'description': 'Features a vibrant always-on AMOLED edge-to-edge curved screen, comprehensive ECG and SpO2 health tracking, sleep monitoring, and GPS navigation. Water-resistant up to 50 meters with customizable fluoroelastomer straps.',
                'price': Decimal('299.99'),
                'discount_price': Decimal('249.99'),
                'image_url': '/static/images/products/smartwatch.svg',
                'stock': 18,
                'is_featured': True,
                'rating': Decimal('4.8'),
                'review_count': 94,
            },
            {
                'name': 'AeroBook Ultra 15-inch Pro Laptop',
                'category': 'Electronics',
                'description': 'Aerospace-grade unibody aluminum design packed with a blazing fast 12-core processor, 32GB unified high-speed RAM, and 1TB NVMe SSD. Features a razor-sharp 4K Retina display, backlit keyboard, and 18-hour battery longevity.',
                'price': Decimal('1299.99'),
                'discount_price': Decimal('1149.99'),
                'image_url': '/static/images/products/laptop.svg',
                'stock': 8,
                'is_featured': True,
                'rating': Decimal('4.9'),
                'review_count': 62,
            },
            {
                'name': 'Velocity Air Performance Running Shoes',
                'category': 'Footwear',
                'description': 'Ultra-breathable engineered knit upper paired with high-energy carbon composite midfoot plate and responsive foam cushioning. Designed for long-distance training and speed with maximum shock absorption.',
                'price': Decimal('149.99'),
                'discount_price': Decimal('119.99'),
                'image_url': '/static/images/products/shoes.svg',
                'stock': 30,
                'is_featured': True,
                'rating': Decimal('4.7'),
                'review_count': 85,
            },
            {
                'name': 'Heritage Full-Grain Leather Messenger Bag',
                'category': 'Bags & Luggage',
                'description': 'Handcrafted from premium oil-waxed full-grain cowhide leather with antique brass hardware and reinforced stitching. Features a padded 16-inch laptop pocket, quick-access front pouches, and an adjustable shoulder strap.',
                'price': Decimal('189.99'),
                'discount_price': Decimal('159.99'),
                'image_url': '/static/images/products/bag.svg',
                'stock': 12,
                'is_featured': True,
                'rating': Decimal('4.9'),
                'review_count': 47,
            },
            {
                'name': 'Urban Commuter Waterproof Backpack',
                'category': 'Bags & Luggage',
                'description': 'Modern minimalist weatherproof backpack constructed with 900D ballistic matte nylon. Features an anti-theft hidden passport pocket, luggage pass-through strap, external USB pass-through port, and waterproof taped zippers.',
                'price': Decimal('89.99'),
                'discount_price': Decimal('74.99'),
                'image_url': '/static/images/products/backpack.svg',
                'stock': 22,
                'is_featured': False,
                'rating': Decimal('4.6'),
                'review_count': 56,
            },
            {
                'name': 'Vortex RGB Mechanical Gaming Keyboard',
                'category': 'Electronics',
                'description': 'Hot-swappable tactile mechanical switches with double-shot PBT keycaps and sound-dampening acoustic silicone padding. Offers dynamic per-key RGB lighting, magnetic wrist rest, and detachable braided braided cable.',
                'price': Decimal('119.99'),
                'discount_price': None,
                'image_url': '/static/images/products/keyboard.svg',
                'stock': 15,
                'is_featured': False,
                'rating': Decimal('4.8'),
                'review_count': 73,
            },
            {
                'name': 'Aviator Polarized Titanium Sunglasses',
                'category': 'Accessories',
                'description': 'Ultra-lightweight aerospace titanium frames fitted with 100% UV400 polarized scratch-resistant gradient lenses. Reduces harsh glare while driving or outdoors while ensuring featherweight all-day comfort.',
                'price': Decimal('79.99'),
                'discount_price': Decimal('59.99'),
                'image_url': '/static/images/products/sunglasses.svg',
                'stock': 25,
                'is_featured': False,
                'rating': Decimal('4.7'),
                'review_count': 39,
            },
            {
                'name': 'Classic StreetStyle Low-Top Canvas Sneakers',
                'category': 'Footwear',
                'description': 'Timeless low-profile silhouette with heavy-duty breathable canvas, vulcanized waffle rubber outsole, and cushioned OrthoLite insole. A versatile streetwear essential for casual everyday comfort.',
                'price': Decimal('69.99'),
                'discount_price': Decimal('54.99'),
                'image_url': '/static/images/products/sneakers.svg',
                'stock': 40,
                'is_featured': False,
                'rating': Decimal('4.6'),
                'review_count': 110,
            },
            {
                'name': 'HydroPeak Insulated Stainless Steel Bottle',
                'category': 'Accessories',
                'description': 'Double-wall vacuum insulation keeps drinks ice cold for 24 hours or piping hot for 12 hours. BPA-free food-grade 18/8 stainless steel with leakproof spout lid and tough scratch-resistant powder coating.',
                'price': Decimal('34.99'),
                'discount_price': Decimal('27.99'),
                'image_url': '/static/images/products/waterbottle.svg',
                'stock': 50,
                'is_featured': False,
                'rating': Decimal('4.9'),
                'review_count': 156,
            },
        ]

        for pdata in products_data:
            cat = cat_objs[pdata['category']]
            product, created = Product.objects.get_or_create(
                name=pdata['name'],
                defaults={
                    'category': cat,
                    'description': pdata['description'],
                    'price': pdata['price'],
                    'discount_price': pdata['discount_price'],
                    'image_url': pdata['image_url'],
                    'stock': pdata['stock'],
                    'is_featured': pdata['is_featured'],
                    'rating': pdata['rating'],
                    'review_count': pdata['review_count'],
                }
            )
            if not created:
                # Update fields if it already exists
                product.image_url = pdata['image_url']
                product.price = pdata['price']
                product.discount_price = pdata['discount_price']
                product.is_featured = pdata['is_featured']
                product.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully populated database with {len(products_data)} products across {len(categories_data)} categories!"))
