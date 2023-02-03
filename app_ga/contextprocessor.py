from app_ga.models import guest_cart2, wishlist
from app_ga.models import cart,myusers


def counter(request):
    cart_count = 0
    if 'username' in request.session:
        username = request.session.get('username')
        user=myusers.objects.get(username=username)
        cartitems=cart.objects.filter(userid = user.id)
        print('lollllllllllll',cartitems)
        
        wish = wishlist.objects.filter(userid = user.id)
        wish = len(wish)
        cart_count = len(cartitems)
        
    else :
        wish = 0
        if 'guest' in request.session:
            session_key = request.session.get('guest')
            gcart = guest_cart2.objects.filter(user_session = session_key)
            cart_count = len(gcart)
    return dict(cart_count=cart_count,wish=wish)

