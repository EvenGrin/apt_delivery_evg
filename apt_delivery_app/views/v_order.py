from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from apt_delivery_app.forms import ChangeOrderForm, ChangeOrderMealForm
from apt_delivery_app.models import Order, Status, Cart, OrderMeal


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


def sub_from_order(request):
    pass
