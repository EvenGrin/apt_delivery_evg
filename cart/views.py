from django.shortcuts import render

from cart.models import Cart


# Create your views here.

def cart(request):
    current_user = request.user.id
    carts = Cart.objects.filter(user__id=current_user)
    context = {'carts': carts}
    return render(request, 'cart/index.html', context)