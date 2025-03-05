from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from apt_delivery_app.forms import ChangeOrderForm
from apt_delivery_app.models import Order, Status, Cart


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


@login_required
def change_order(request, order_id=0):
    if request.method == "POST":
        print(request.POST)
        form = ChangeOrderForm(request.POST)
        if form.is_valid():
            pass
    else:
        get = get_object_or_404(Order, id=order_id)
        form = ChangeOrderForm(instance=get)
        print()
    context = {
        'form': form
    }
    return render(request, 'order/change_order.html', context=context)
