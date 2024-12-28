from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from order.models import Order


@login_required
def deliver_order_list(request):
    context = {}
    deliver = request.user # Получаем авторизованного курьера
    context['orders'] = Order.objects.filter(deliver=deliver) # Фильтруем заказы

    # Другие варианты фильтрации:
    # orders = Order.objects.filter(status='ready_for_delivery') # Заказы без курьера
    # orders = Order.objects.all() # Все заказы

    return render(request, 'deliver/order_list.html', context)

@login_required
def deliver_update_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id, deliver=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        return HttpResponseRedirect(reverse('deliver_order_list')) # Перенаправление на список заказов

    context = {'order': order, 'statuses': ['in_transit', 'delivered', 'problems']}
    return render(request, 'deliver/update_status.html', context)