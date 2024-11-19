from django.shortcuts import render

from order.models import Order, OrderMeal


def order(request):
    orders = Order.objects.all().filter(user=request.user).order_by('-date_create')
    context = {'orders': orders}
    return render(request, 'order/index.html', context)
