from django.db.models import Prefetch
from django.shortcuts import render

from cart.models import Cart
from .models import Meal, Category


def meal_list(request):
    context = {}
    context['categories'] = Category.objects.prefetch_related(
        Prefetch(
            'meals',
            queryset=Meal.objects.order_by('price'),  # Сортировка блюд по возрастанию цены
            to_attr='ordered_meals'
        )
    )
    if request.user.is_authenticated:
        context['cart_count'] = Cart.objects.filter(user=request.user).count()
        cart_items = Cart.objects.filter(user=request.user, meal__in=Meal.objects.all()).values('meal_id', 'quantity')
        context['cart_items'] = cart_items
        context['cart_items_id'] = [cart_item['meal_id'] for cart_item in cart_items]

    return render(request, 'home/index.html', context)
