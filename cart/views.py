from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required  # Для авторизации
from cart.models import Cart
from home.models import Meal


# Create your views here.


def cart(request):
    current_user = request.user.id
    carts = Cart.objects.filter(user__id=current_user)
    context = {'carts': carts}
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