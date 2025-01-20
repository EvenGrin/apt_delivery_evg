from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from order.models import Order, Status


@login_required
def take_order(request, order='-date_create', filter=0):
    context = {}
    context['order'] = order
    context['filter'] = filter
    context['orders'] = Order.objects.filter(status__id__in=[1, 2, 4]).order_by('-date_create')
    return render(request, 'deliver/order_list.html', context)

@login_required
def change_status_order(request):
    context = {}
    context['orders'] = Order.objects.filter(deliver=request.user).order_by('-date_create')
    return render(request, 'deliver/order_list.html', context)

@login_required
def order_list(request, order='-date_create', filter=0):
    context = {}
    context['order'] = order
    context['filter'] = filter
    context['statuses'] = Status.objects.all()
    orders = Order.objects.filter(status__in=[1,2,4])  # Фильтруем заказы
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
