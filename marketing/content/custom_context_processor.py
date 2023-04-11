from .models import *

def content_category(request):
    categories = Category.objects.all()

    return {'categories':categories}

def cart_count(request):
    cart_quantity = 0
    if request.user.is_authenticated:
        user = request.user
        cart_quantity = Cart.objects.filter(user=user).count()
    else:
        pass
    
    return {'cart_quantity':cart_quantity}