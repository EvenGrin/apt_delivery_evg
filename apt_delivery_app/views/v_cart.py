# Create your views here.
import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from apt_delivery_app.forms import CreateOrderForm
from apt_delivery_app.models import Cart, Order, Cabinet, OrderMeal, Meal


@login_required
def make_order(request):
    if request.method == 'POST':
        cab_pk = request.POST.get("cab")  # Получаем идентификатор кабинета
        form = CreateOrderForm(request.POST)

        if form.is_valid():
            cart_items = Cart.objects.filter(user=request.user)  # Получаем элементы корзины пользователя

            if not cart_items:
                messages.error(request,"Корзина пуста! Пожалуйста, добавьте блюда.")  # Сообщение об ошибке, если корзина пустая
                print(messages.error)
                return redirect(reverse('cart'))  # Перенаправление на страницу корзины

            try:
                with transaction.atomic():  # Начинаем транзакцию для атомарности операций
                    order = Order(user=request.user)
                    order.cab = Cabinet.objects.get(pk=cab_pk)
                    order.order_date = form.cleaned_data['order_date']
                    order.user_comment = form.cleaned_data['user_comment']
                    order.save()

                    for cart_item in cart_items:
                        meal = cart_item.meal
                        required_amount = cart_item.quantity

                        if meal.quantity < required_amount:
                            raise ValidationError(
                                f"Недостаточно товара '{meal.name}'. Доступно: {meal.quantity}, требуется: {required_amount}")

                        OrderMeal.objects.create(
                            order=order,
                            meal=meal,
                            amount=required_amount
                        )

                        meal.quantity -= required_amount
                        meal.save()

                        cart_item.delete()  # Удаляем элемент из корзины после успешного создания заказа

                return redirect(reverse('order'))  # Переходим на страницу заказов, если всё прошло успешно
            except ValidationError as e:
                messages.error(request,
                               f"Ошибка при оформлении заказа: {e}")  # Сообщение об ошибке при нехватке товаров
                return redirect(reverse('cart'))  # Перенаправление обратно в корзину для коррекции заказа
            except Exception as e:
                messages.error(request,
                               f"Произошла ошибка при обработке заказа: {e}")  # Обработка других возможных исключений
                return redirect(reverse('cart'))  # Перенаправление обратно в корзину

    else:
        form = CreateOrderForm()

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
    context['cabs'] = sorted(Cabinet.objects.all(), key=sort_cabs)
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

    meal_id = request.POST.get('meal_id')
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

        cart_item.quantity += quantity_change

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

@csrf_exempt
@login_required
def add_to_cart(request):
    return update_cart_item(request, 'add')

@csrf_exempt
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

@csrf_exempt
@login_required
def remove_from_cart(request):
    if request.method == 'POST':
        meal_id = request.POST.get('meal_id')
        Cart.objects.all().filter(user=request.user, meal=meal_id).delete()
        # print('удаление из корзины'+ meal_id)
        return JsonResponse(get_cart_data(request.user))


@login_required
def update_cart_view(request):
  return JsonResponse(get_cart_data(request.user))
