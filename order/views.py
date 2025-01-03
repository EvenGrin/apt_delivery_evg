from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from order.models import Order, OrderMeal

@login_required
def order(request):
    context = {}
    context['cart_count'] = Cart.objects.filter(user=request.user).count()
    orders = Order.objects.all().filter(user=request.user).order_by('-date_create')
    context['orders'] = orders
    return render(request, 'order/index.html', context)
