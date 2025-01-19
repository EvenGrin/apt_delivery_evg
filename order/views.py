from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from order.models import Order, OrderMeal, Status


@login_required
def order(request, order='-date_create', filter=0):
    context = {}
    context['order'] = order
    context['filter'] = filter
    context['statuses'] = Status.objects.all()
    context['cart_count'] = Cart.objects.filter(user=request.user).count()
    orders = Order.objects.all().filter(user=request.user).order_by(order)
    if filter:
        orders = orders.filter(status__id=filter)
    context['orders'] = orders
    return render(request, 'order/index.html', context)
