from app_ga.models import guest_cart2, wishlist
from app_ga.models import cart


def counter(request):
    cart_count = 0
    if 'username' in request.session:
        Cart = cart.objects.all()
        
        wish = wishlist.objects.all()
        wish = len(wish)
        cart_count = len(Cart)
        
    else :
        wish = None
        gcart = guest_cart2.objects.all()
        cart_count = len(gcart)
    return dict(cart_count=cart_count,wish=wish)

