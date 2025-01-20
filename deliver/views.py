from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from order.models import Order, Status


@login_required
def take_order(request):
    context = {}
    context['orders'] = Order.objects.filter(status__name='').order_by('-date_create')
    return render(request, 'deliver/order_list.html', context)


@login_required
def deliver_order_list(request, order='-date_create', filter=0):
    context = {}
    context['order'] = order
    context['filter'] = filter
    context['statuses'] = Status.objects.all()

    deliver = request.user  # Получаем авторизованного курьера
    context['orders'] = Order.objects.filter(status=4)  # Фильтруем заказы

    # Другие варианты фильтрации:
    # orders = Order.objects.filter(status='ready_for_delivery') # Заказы без курьера
    # orders = Order.objects.all() # Все заказы
    orders = Order.objects.all().order_by(order)
    if filter:
        orders = orders.filter(status__id=filter)
    context['orders'] = orders
    return render(request, 'deliver/order_list.html', context)




@login_required
def deliver_update_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id, deliver=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        return HttpResponseRedirect(reverse('deliver_order_list'))  # Перенаправление на список заказов

    context = {'order': order, 'statuses': ['in_transit', 'delivered', 'problems']}
    return render(request, 'deliver/update_status.html', context)
