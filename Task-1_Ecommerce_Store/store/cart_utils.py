from .models import Cart, CartItem


def get_or_create_cart(request):
    """
    Retrieve or create the shopping cart for either a logged-in user or anonymous session.
    """
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        # If there was a session cart created while user was browsing as a guest, merge it into the user's cart
        session_key = request.session.session_key
        if session_key:
            session_cart = Cart.objects.filter(session_key=session_key, user=None).first()
            if session_cart and session_cart != cart:
                for item in session_cart.items.all():
                    existing_item = CartItem.objects.filter(cart=cart, product=item.product).first()
                    if existing_item:
                        existing_item.quantity += item.quantity
                        existing_item.save()
                    else:
                        item.cart = cart
                        item.save()
                session_cart.delete()
        return cart
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key, user=None)
        return cart
