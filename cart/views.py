import re

from django.contrib.auth.decorators import login_required  # Для авторизации
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from cart.forms import CreateOrderForm
from cart.models import Cart, Cabinet
from home.models import Meal
from home.views import meal_list
from order.models import OrderMeal, Order


# Create your views here.
@login_required
def make_order(request):
    if request.method == 'POST':
        cab = request.POST["cab"]
        form = CreateOrderForm(user=request.user, data=request.POST)
        meals = Cart.objects.all().filter(user=request.user)
        if form.is_valid() and meals:
            order = Order(user=request.user)
            order.cab = Cabinet.objects.get(pk=cab)
            order.order_date = request.POST['order_date']
            order.save()
            for p in meals:
                op = OrderMeal(order=order, meal=p.meal, amount=p.quantity)
                op.save()
                p.delete()
            return redirect(reverse('cart'))

    else:
        form = CreateOrderForm(user=request.user)
    return form


def get_cart_data(user):
    total = sum(item.meal.price * item.quantity for item in Cart.objects.filter(user=user))
    amount = Cart.objects.filter(user=user).aggregate(Sum('quantity'))['quantity__sum'] or 0
    cart_count = Cart.objects.filter(user=user).count()
    return {
        'total_price': total,
        'amount': amount,
        'cart_count': cart_count
    }

def sort_cabs(cabinet):
    """Функция для определения ключа сортировки."""
    if re.match(r'^\d', cabinet.num):
        return (1, cabinet.num)  # Сначала сортировка по 1 (цифровые), затем по номеру
    else:
        return (0, cabinet.num)  # Сначала сортировка по 0 (нецифровые), затем по номеру
@login_required
def cart(request):
    context = get_cart_data(request.user)
    cabs = Cabinet.objects.all()
    sorted_cabs = sorted(cabs, key=sort_cabs)

    context['cabs'] = sorted_cabs
    context['carts'] = Cart.objects.filter(user=request.user)
    #
    if request.method == 'POST':
        form = make_order(request)
        if isinstance(form, HttpResponseRedirect):
            return form
        else:
            context['form'] = form
    else:
        form = make_order(request)
        context['form'] = form

    return render(request, 'cart/index.html', context)


@login_required
def update_cart_item(request, action):
    """Обновляет количество товара в корзине."""
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    meal_id = request.GET.get('meal_id')
    meal = Meal.objects.get(pk=meal_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, meal=meal, defaults={'quantity': 0})
    quantity_change = 1 if action == 'add' else -1 if action == 'sub' else 0

    if action == 'add':
        if cart_item.quantity >= meal.quantity:
            return JsonResponse({
                'success': True,
                'cart_count': Cart.objects.filter(user=request.user).count(),
                'quantity': 'Больше нельзя'
            })
        cart_item.quantity += quantity_change

    if action == 'sub':
        if cart_item.quantity == 0:
            return JsonResponse({
                'success': True,
                'cart_count': Cart.objects.filter(user=request.user).count(),
                'quantity': 'Больше не в корзине'
            })

        cart_item.quantity += quantity_change;

    if cart_item.quantity > 0:
        cart_item.save()
    else:
        cart_item.delete()

    cart_data = get_cart_data(request.user)
    return JsonResponse({
        'success': True,
        'quantity': cart_item.quantity,
        'total_amount': cart_item.total_amount if hasattr(cart_item, 'total_amount') else None,
        **cart_data
    })


@login_required
def add_to_cart(request):
    return update_cart_item(request, 'add')


@login_required
def sub_from_cart(request):
    return update_cart_item(request, 'sub')


@login_required
def cart_empty(request):
    if request.method == 'GET':
        Cart.objects.filter(user=request.user).delete()
        return HttpResponse(
            "<div class='alert alert-danger text-center'>В корзине ничего нет</div>")
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def remove_from_cart(request):
    if request.method == 'GET':
        meal_id = request.GET.get('meal_id')
        Cart.objects.all().filter(user=request.user, meal=meal_id).delete()
        print('удаление из корзины'+ meal_id)
        return JsonResponse(get_cart_data(request.user))


@login_required
def update_cart_view(request):
  return JsonResponse(get_cart_data(request.user))