from django import template
from cart.models import Cart

register = template.Library()


@register.simple_tag(takes_context=True)
def cart_total_items(context):
    """Retourne le nombre total d'articles dans le panier."""
    request = context.get("request")
    if not request:
        return 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            return cart.total_items
        except Cart.DoesNotExist:
            return 0
    else:
        session_key = request.session.session_key
        if session_key:
            try:
                cart = Cart.objects.get(session_key=session_key, user=None)
                return cart.total_items
            except Cart.DoesNotExist:
                return 0
    return 0
