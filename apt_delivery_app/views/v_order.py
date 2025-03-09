from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.forms import inlineformset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from apt_delivery_app.forms import ChangeOrderForm, ChangeOrderMealForm
from apt_delivery_app.models import Order, Status, Cart, OrderMeal, Meal


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
def change_order(request, pk=0):
    # Получаем объект заказа или возвращаем 404, если он не найден
    order = get_object_or_404(Order, pk=pk)

    if request.method == "POST":
        # Создаем формы с данными из POST-запроса
        form = ChangeOrderForm(request.POST, instance=order)
        OrderMealFormSet = inlineformset_factory(Order, OrderMeal, form=ChangeOrderMealForm, extra=1)
        formset = OrderMealFormSet(request.POST, instance=order)

        if form.is_valid() and formset.is_valid():
            # Сохраняем изменения в заказе
            order = form.save()
            formset.save()  # Сохраняем изменения в блюдах заказа
            return redirect('order')  # Перенаправление после успешного сохранения
    else:
        # Если метод GET, создаем формы с текущими данными заказа
        form = ChangeOrderForm(instance=order)
        OrderMealFormSet = inlineformset_factory(Order, OrderMeal, form=ChangeOrderMealForm, extra=1)
        formset = OrderMealFormSet(instance=order)

    context = {
        'form': form,
        'formset': formset,
        'order': order,
    }
    return render(request, 'order/change_order.html', context=context)


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
