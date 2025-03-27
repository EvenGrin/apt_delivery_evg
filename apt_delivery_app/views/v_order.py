import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncDate
from django.forms import inlineformset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from apt_delivery_app.forms import ChangeOrderForm, ChangeOrderMealForm
from apt_delivery_app.models import Order, Status, Cart, OrderMeal, Cabinet, Meal
from apt_delivery_app.views import sort_cabs


@login_required
def order(request, order_by='-date_create', filter=0):
    context = {}
    context['order_by'] = order_by
    context['filter'] = filter
    context['statuses'] = Status.objects.all()
    context['cart_count'] = Cart.objects.filter(user=request.user).count()
    orders = Order.objects.all().filter(user=request.user).order_by(order_by)
    if filter:
        orders = orders.filter(status__id=filter)
    context['orders'] = orders
    context['cabs'] = sorted(Cabinet.objects.all(), key=sort_cabs)
    return render(request, 'order/index.html', context)


@csrf_protect
@login_required
def order_update(request):
    post = request.POST
    if request.method == "POST":
        order = Order.objects.get(pk=request.POST.get('pk'))
        order.user_comment = post.get('user_comment')
        order.order_date = post.get('order_date')
        order.cab = Cabinet.objects.get(pk=post.get('cab'))
        order.save()
    data = {
        'user_comment': order.user_comment,
        'order_date': order.order_date,
        'cab': order.cab,
    }
    return HttpResponse(data)
    # return render(request, 'order/order_update.html', context=context)


def get_cart_data(user):
    total = sum(item.meal.price * item.quantity for item in Cart.objects.filter(user=user))
    amount = Cart.objects.filter(user=user).aggregate(Sum('quantity'))['quantity__sum'] or 0
    cart_count = Cart.objects.filter(user=user).count()
    return {
        'total_price': total,
        'amount': amount,
        'cart_count': cart_count
    }


@login_required
def update_order_item(request, action):
    meal_id = request.POST.get('meal_id')
    meal = Meal.objects.get(pk=meal_id)
    order_id = request.POST.get('order_id')
    order_item = OrderMeal.objects.get(order=order_id, meal=meal_id)
    quantity_change = 1 if action == 'add' else -1 if action == 'sub' else 0

    if action == 'add':
        if order_item.amount >= meal.quantity:
            return JsonResponse({
                'success': True,
                # 'cart_count': Cart.objects.filter(user=request.user).count(),
                'quantity': 'Больше нельзя'
            })
        order_item.amount += quantity_change

    if action == 'sub':
        if order_item.amount == 0:
            return JsonResponse({
                'success': True,
                # 'cart_count': Cart.objects.filter(user=request.user).count(),
                'quantity': 'Больше не в корзине'
            })
        order_item.amount += quantity_change

    if order_item.amount > 0:
        order_item.save()
    else:
        order_item.delete()

    cart_data = get_cart_data(request.user)
    return JsonResponse({
        'success': True,
        'quantity': order_item.amount,
        'total_amount': order_item.total_amount if hasattr(order_item, 'total_amount') else None,
        **cart_data
    })


@csrf_exempt
@login_required
def add_to_order(request):
    print(123)
    return update_order_item(request, 'add')


@csrf_exempt
@login_required
def sub_from_order(request):
    print('sub_from_cart')
    return update_order_item(request, 'sub')
