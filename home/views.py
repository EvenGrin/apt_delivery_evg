
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from cart.models import Cart
from .models import Meal, Category

def pagination(request, categories):
    if request.method == 'GET':
        category_id = request.GET.get('category')
        if category_id:
            meals = Meal.objects.filter(category__id=category_id)
        else:
            meals = Meal.objects.all()
        context = {'meals': meals, 'categories': categories}
        return render(request, 'home/index.html', context)

def meal_list(request):
    context = {}

    context['categories'] = Category.objects.annotate(meal_count=Count('meals'))
    meals = Meal.objects.all()

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user, meal__in=meals).values('meal_id', 'quantity')

        context['cart_items'] = cart_items
        context['cart_items_id'] = [cart_item['meal_id'] for cart_item in cart_items]

    # if request.user.is_authenticated:
    #     for meal in meals:
    #         cart = Cart.objects.filter(user=request.user, meal=meal).first()
    #         meal.cart = cart.quantity if cart else 0

    # pagination(request, categories)
    return render(request, 'home/index.html', context)


def menu(request):
    context = {}

    context['categories'] = Category.objects.annotate(meal_count=Count('meals'))
    meals = Meal.objects.all()

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user, meal__in=meals).values('meal_id', 'quantity')

        context['cart_items'] = cart_items
        context['cart_items_id'] = [cart_item['meal_id'] for cart_item in cart_items]


    return render(request, 'home/index.html', context)



def meal_list_ajax(request):
    category_id = request.GET.get('category')

    if category_id:
        meals = Meal.objects.filter(category__id=category_id)
        if category_id == '0':
            meals = Meal.objects.all()
    else:
        meals = Meal.objects.all()
    return render(request, 'home/elements/meals_cards.html', {'meals': meals})
