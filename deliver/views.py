from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from order.models import Order, Status

limit = 10  # ограничение количества взятия заказов


@login_required
def take_order(request):
    order_id = request.GET['order_id']
    count = Order.objects.filter(~Q(status=7), deliver=request.user).count()
    if (Order.objects.filter(id=order_id, cab=0)):
        return JsonResponse({'message': 'Нельзя взять заказы с самовыносом', 'count': count})
    if count < 10:
        order = Order.objects.filter(id=order_id).update(deliver=request.user)
        message = 'Взято заказов ' + str(count + 1)
        return JsonResponse({'message': message, 'count': count})
    else:
        return JsonResponse({'message': 'Уже взято 10 заказов', 'count': count})






@login_required
def update_status(request):
    order_id = request.GET['order_id']
    if Order.objects.filter(id=order_id, status=4):
        order = Order.objects.filter(id=order_id).update(status=6)
        return JsonResponse({'class_add': 'delivered', 'class_remove': 'in_way', 'html': 'Изменить на джоставлен'})
    elif Order.objects.filter(id=order_id, status=6):
        order = Order.objects.filter(id=order_id).update(status=7)
        return JsonResponse({'class_add': 'btn-outline', 'class_remove': 'delivered', 'html': 'Изменен'})


@login_required
def order_list(request, order='-date_create', filter=0):
    context = {}
    context['order'] = order
    context['filter'] = filter
    context['count'] = Order.objects.filter(deliver=request.user).count()

    # заказы, которые не самовынос, без курьера, со статусом новый подтвержден, собран
    context['orders'] = Order.objects.filter(~Q(cab=0), status__in=[1, 2, 4], deliver=None).order_by(
        order)  # Фильтруем заказы
    return render(request, 'deliver/order_list.html', context)


@login_required
def deliver_orders(request, order='-date_create', filter=0):
    context = {}
    context['order'] = order
    context['filter'] = filter
    context['count'] = Order.objects.filter(deliver=request.user).count()
    context['statuses'] = Status.objects.filter(~Q(id=5))
    orders = Order.objects.filter(deliver=request.user).order_by(order)
    # Все заказы
    if filter:
        orders = Order.objects.filter(deliver=request.user, status=filter).order_by(order)
    context['orders'] = orders  # Фильтруем заказы
    return render(request, 'deliver/order_list.html', context)
