from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from apt_delivery_app.decorators import group_required
from apt_delivery_app.models import Order, Status

limit = 10  # ограничение количества взятия заказов


@login_required
def take_order(request):
    order_id = request.GET['order_id']
    count = Order.objects.filter(status__in=[4], deliver=request.user).count()
    # print(count)
    if (Order.objects.filter(id=order_id, cab=0)):
        return JsonResponse({'message': 'Нельзя взять заказы с самовыносом', 'count': count})
    if count < 5:
        order = Order.objects.filter(id=order_id).update(deliver=request.user)
        message = 'Взято заказов ' + str(count + 1)
        return JsonResponse({'message': message, 'count': count+1})
    else:
        return JsonResponse({'message': 'Уже взято 5 заказов', 'count': count})


@login_required
def update_status(request):
    order_id = request.GET['order_id']
    if Order.objects.filter(id=order_id, status=4):
        order = Order.objects.filter(id=order_id).update(status=6)
        status = Order.objects.values('status__id', 'status__name').get(id=order_id)
        return JsonResponse({'class_add': 'delivered, btn-outline-success', 'class_remove': 'in_way, btn-primary',
                             'html': 'Изменен на в пути', 'status': status})
    elif Order.objects.filter(id=order_id, status=6):
        order = Order.objects.filter(id=order_id).update(status=7)
        status = Order.objects.values('status__id', 'status__name').get(id=order_id)
        # print(status)
        return JsonResponse({'class_add': 'btn-outline-success', 'class_remove': 'delivered, btn-primary',
                             'html': 'Изменен на доставлен', 'status': status})
    return JsonResponse({})


@login_required
def take_order_list(request, order='-date_create', filter=0):
    context = {}
    context['order'] = order
    context['filter'] = filter
    count = Order.objects.filter(status__in=[4], deliver=request.user).count()
    context['count'] = 'взято '+str(count)
    # заказы, которые не самовынос, без курьера, со статусом новый подтвержден, собран
    context['orders'] = Order.objects.filter(~Q(cab=0), status__in=[4], deliver=None).order_by(
        order)  # Фильтруем заказы
    return render(request, 'deliver/take_order_list.html', context)

@group_required('deliver')
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