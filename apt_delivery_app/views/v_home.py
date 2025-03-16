from datetime import date

from django.db.models import Prefetch, Exists
from django.shortcuts import render
from django.utils import timezone

from apt_delivery_app.models import Meal, Category, Cart, Menu


def meal_list(request):
    global search
    context = {}
    # Получение текущей даты
    today = timezone.now().date()

    # Получение всех блюд
    all_meals = Meal.objects.all()

    # Получение всех блюд, присутствующих в меню на сегодня
    try:
        menu_today = Menu.objects.get(date=today)
    except Menu.DoesNotExist:
        menu_today = None

    # Если меню на сегодня существует, получаем все блюда из него
    if menu_today:
        meals_in_menu_today = menu_today.meal.all()
    else:
        meals_in_menu_today = []

    # Выводим все блюда с указанием наличия в меню
    # for meal in all_meals:
    #     print(Menu.objects.filter(date=today))
        # if meal in meals_in_menu_today:
        #     print(f"{meal.name}: Есть в меню")
        # else:
        #     print(f"{meal.name}: Нет в меню")
    if request.method == "GET":
        context['search'] = request.GET.get('q')
        if context['search']:
            search_result = Meal.objects.filter(name__iregex=context['search'])
            context['search_result'] = search_result
            context['search_count'] = search_result.count()
            context['search_count_all'] = Meal.objects.count()
    context['categories'] = Category.objects.all()
    category = context['categories'].prefetch_related(
        Prefetch(
            'meal_set',
            queryset=Meal.objects.order_by('price'),  # Сортировка блюд по возрастанию цены
            to_attr='ordered_meals'
        )
    )
    context['meals'] = category
    if request.user.is_authenticated:
        context['cart_count'] = Cart.objects.filter(user=request.user).count()
        cart_items = Cart.objects.filter(user=request.user, meal__in=Meal.objects.all()).values('meal_id', 'quantity')
        context['cart_items'] = cart_items
        context['cart_items_id'] = [cart_item['meal_id'] for cart_item in cart_items]

    return render(request, 'home/index.html', context)


def menu(request):
    menu_list = Menu.objects.filter(date=date.today()).prefetch_related('meal')
    # for m in menu_list:
    #     print(m.__dict__)
    # Создаем словарь для хранения блюд по категориям
    categorized_meals = {}

    for m in menu_list:
        meals = m.meal.all().order_by('category__id')
        for meal in meals:
            if meal.category not in categorized_meals:
                categorized_meals[meal.category] = []
            categorized_meals[meal.category].append(meal)
    # print(categorized_meals)
    context = {
        'categories': Category.objects.all(),
        'categorized_meals': categorized_meals,
        'date': date
    }
    return render(request, 'home/menu.html', context=context)
