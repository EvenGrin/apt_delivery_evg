from django.contrib.auth.decorators import login_required  # Для авторизации
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from cart.forms import CreateOrderForm
from cart.models import Cart, Cabinet
from home.models import Meal
from order.models import OrderMeal, Order


# Create your views here.


def cart(request):

    current_user = request.user.id
    cabs = Cabinet.objects.all().order_by("num")
    carts = Cart.objects.filter(user__id=current_user)

    if request.method == 'POST':
        form = CreateOrderForm(request.POST)
        if request.user.check_password(request.POST['password']):
            order = Order(user=request.user)
            print(order)
            order.save()
            products = Cart.objects.all().filter(user=request.user)
            for p in products:

                op = OrderMeal(order=order, meal=p.meal, amount=p.quantity)
                op.save()
                p.delete()
            return HttpResponseRedirect('orders')
        else:
            form.add_error('password', 'не верный пароль')
    else:
        form = CreateOrderForm()
    context = {'carts': carts,
               'cabs': cabs,
               'form': form}
    return render(request, 'cart/index.html', context)


@login_required  # Требуется авторизация
def add_to_cart(request):
    if request.method == 'GET':
        meal_id = request.GET.get('meal_id')
        quantity = int(request.GET.get('quantity', 1))
        print(meal_id, quantity)
        try:
            meal = Meal.objects.get(pk=meal_id)
        except Meal.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)

        try:
            cart_item = Cart.objects.get(user=request.user, meal=meal)
            cart_item.quantity += quantity
            cart_item.save()
        except Cart.DoesNotExist:
            Cart.objects.create(user=request.user, meal=meal, quantity=quantity)

        return JsonResponse({'success': True, 'cart_count': Cart.objects.filter(user=request.user).count()})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def cart_empty(request):
    if request.method == 'GET':
        carts = Cart.objects.filter(user__id=request.user.id)
        carts.delete()
        return HttpResponse("<div class='alert alert-danger text-center'>В корзине ничего нет</div>")
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def remove_from_cart(request):
    if request.method == 'GET':
        meal_id = request.GET.get('meal_id')
        row = Cart.objects.all().filter(user=request.user, meal=meal_id)
        print(row)
        row.delete()
        return HttpResponse("<span class='error-count'>Товар в корзине отсутствует!</span>")
