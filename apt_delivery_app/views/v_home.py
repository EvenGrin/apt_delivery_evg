from datetime import date

from django.db.models import Prefetch, Exists, OuterRef, Case, When, Q, Value, CharField
from django.shortcuts import render
from django.utils import timezone

from apt_delivery_app.models import Meal, Category, Cart, Menu


def search_queryset(queryset, search_string):
    # Разделяем строку поиска на отдельные слова
    search_words = search_string.split()

    # Формируем сложный запрос с использованием оператора OR для каждого слова
    query = Q()
    for word in search_words:
        query |= Q(name__iregex=word) | Q(category__name__iregex=word)

    # Применяем сформированный запрос к queryset
    search_result = queryset.filter(query)

    return search_result


def meal_list(request):
    global search
    context = {}
    # Аннотируем блюда наличием в меню
    # Проверяем наличие блюда в меню на сегодня
    menu_exists_subquery = Meal.objects.filter(pk=OuterRef('pk')).filter(menu__date=timezone.now().date())

    # Проверяем, закончилось ли блюдо (если remaining_portions == 0)
    finished_subquery = Meal.objects.filter(pk=OuterRef('pk')).filter(quantity=0)

    # Формируем аннотации для трех состояний
    queryset = Meal.objects.annotate(
        in_today_menu=Exists(menu_exists_subquery),
        finished=Exists(finished_subquery),
        status=Case(
            When(in_today_menu=True, then=Value("Есть в меню")),
            When(Q(in_today_menu=True, finished=True), then=Value("Закончилось")),
            default=Value("Нет в меню"),
            output_field=CharField(),
        ),
    ).order_by('-in_today_menu', 'finished', 'price')


    if request.method == "GET":
        context['search'] = request.GET.get('q')
        if context['search']:
            search_result = search_queryset(queryset, context['search'])
            context['search_result'] = search_result
            context['search_count'] = search_result.count()
            context['search_count_all'] = Meal.objects.count()
    context['categories'] = Category.objects.all()

    category = context['categories'].prefetch_related(
        Prefetch(
            'meal_set',
            queryset=queryset,  # Сортировка блюд по возрастанию цены
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
    menu_exists_subquery = Meal.objects.filter(pk=OuterRef('pk')).filter(menu__date=date.today())

    # Проверяем, закончилось ли блюдо (если remaining_portions == 0)
    finished_subquery = Meal.objects.filter(pk=OuterRef('pk')).filter(quantity=0)

    # Формируем аннотации для трех состояний
    menu_list = Menu.objects.filter(date=date.today()).prefetch_related(
        Prefetch(
            'meal',
            queryset=Meal.objects.annotate(
                in_today_menu=Exists(menu_exists_subquery),
                finished=Exists(finished_subquery),
                status=Case(
                    When(Q(in_today_menu=True, finished=True), then=Value("Закончилось")),
                    When(in_today_menu=True, then=Value("Есть в меню")),
                    default=Value("Нет в меню"),
                    output_field=CharField(),
                ),
            ).order_by('finished', 'category__id'),
            to_attr='annotated_meals'
        )
    )
    categorized_meals = {}
    for m in menu_list:
        for meal in m.annotated_meals:
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
