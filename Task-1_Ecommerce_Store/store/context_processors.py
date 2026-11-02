from .models import Category
from .cart_utils import get_or_create_cart


def cart_and_categories(request):
    """
    Context processor to inject categories, cart item count, and active cart into all templates.
    """
    try:
        categories = Category.objects.all()
    except Exception:
        categories = []

    cart_item_count = 0
    cart_total = 0
    cart = None

    try:
        cart = get_or_create_cart(request)
        if cart:
            cart_item_count = cart.total_items
            cart_total = cart.total_price
    except Exception:
        pass

    return {
        'nav_categories': categories,
        'cart_item_count': cart_item_count,
        'cart_total': cart_total,
        'global_cart': cart,
    }
