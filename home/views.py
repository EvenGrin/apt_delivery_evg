from django.http import JsonResponse
from django.shortcuts import render
from cart.models import Cart
from .models import Meal, Category


def meal_list(request):
    meals = Meal.objects.all()
    categories = Category.objects.all()
    context = {'meals': meals,
               }
    if request.method == 'GET':
        category_id = request.GET.get('category')
        if category_id:
            meals = Meal.objects.filter(category__id=category_id)
        else:
            meals = Meal.objects.all()
        if request.user.is_authenticated:
            for meal in meals:
                cart = Cart.objects.filter(user=request.user, meal=meal).first()
                meal.cart = cart.quantity if cart else 0

        context = {'meals': meals, 'categories': categories}
        return render(request, 'home/index.html', context)
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
