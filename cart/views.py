from django.contrib.auth.decorators import login_required  # Для авторизации
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from cart.forms import CreateOrderForm
from cart.models import Cart, Cabinet
from home.models import Meal
from order.models import OrderMeal, Order


# Create your views here.


def cart(request):
    current_user = request.user.id
    cabs = Cabinet.objects.all().order_by("num")
    carts = Cart.objects.filter(user__id=current_user)
    # заказы
    if request.method == 'POST':
        cab = request.POST["cab"]
        form = CreateOrderForm(request.POST)

        if request.user.check_password(request.POST['password']):
            order = Order(user=request.user)
            order.cab = Cabinet.objects.get(pk=cab)
            order.save()
            meals = Cart.objects.all().filter(user=request.user)
            for p in meals:
                op = OrderMeal(order=order, meal=p.meal, amount=p.quantity)
                op.save()
                p.delete()
            return redirect('order')
        else:
            form.add_error('password', 'не верный пароль')
    else:
        form = CreateOrderForm()
    context = {'carts': carts,
               'cabs': cabs,
               'form': form}
    return render(request, 'cart/index.html', context)


@login_required
def add_to_cart(request):
    if request.method == 'GET':
        id = request.GET.get('meal_id')
        row = Cart.objects.all().filter(user=request.user, meal=id)
        meal = Meal.objects.get(pk=id)
        if len(row):
            row = row[0]
            if row.quantity >= meal.quantity:
                return JsonResponse({'success': True, 'cart_count': Cart.objects.filter(
                    user=request.user).count(), 'quantity': 'Больше незя'})
            row.quantity += 1
        else:
            row = Cart(user=request.user, meal=meal, quantity=1)

        row.save()
        return JsonResponse({'success': True,
                             'quantity': row.quantity,
                             'cart_count': (
                                 Cart.objects.filter(
                                     user=request.user).count())})


def cart_empty(request):
    if request.method == 'GET':
        carts = Cart.objects.filter(user__id=request.user.id)
        carts.delete()
        return HttpResponse(
            "<div class='alert alert-danger text-center'>В корзине ничего нет</div>")
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def remove_from_cart(request):
    if request.method == 'GET':
        meal_id = request.GET.get('meal_id')
        row = Cart.objects.all().filter(user=request.user, meal=meal_id)
        print(row)
        row.delete()
        return HttpResponse("<span class='error-count'>Товар в корзине отсутствует!</span>")
