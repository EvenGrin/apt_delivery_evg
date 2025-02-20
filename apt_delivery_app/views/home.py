from django.db.models import Prefetch
from django.shortcuts import render

from apt_delivery_app.models import Meal, Category, Cart


def meal_list(request):
    global search

    context = {}
    if request.method == "GET":
        context['search'] = request.GET.get('q')
        if context['search']:
            search_result = Meal.objects.filter(name__iregex=context['search'])
            context['search_result'] = search_result
            context['search_count'] = search_result.count()
            context['search_count_all'] = Meal.objects.count()
    context['categories'] = Category.objects.prefetch_related(
        Prefetch(
            'meal_set',
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