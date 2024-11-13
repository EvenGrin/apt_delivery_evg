from django.http import JsonResponse
from django.shortcuts import render

from .models import Meal, Category


def meal_list(request):
    if request.method == 'GET':
        category_id = request.GET.get('category')
        if category_id:
            meals = Meal.objects.filter(category__id=category_id)
        else:
            meals = Meal.objects.all()
        categories = Category.objects.all()
        context = {'meals': meals,
                   'categories': categories}
        # Отдаем HTML-код списка товаров
        return render(request, 'home/index.html', context)

    elif request.method == 'POST':
        # (Этот код будет добавлен позже)
        return JsonResponse({'success': True})


def meal_list_ajax(request):
    category_id = request.GET.get('category')

    if category_id:
        meals = Meal.objects.filter(category__id=category_id)
        if category_id == '0':
            meals = Meal.objects.all()
    else:
        meals = Meal.objects.all()
    return render(request, 'home/elements/meals_cards.html', {'meals': meals})
