from django.shortcuts import render

from home import models


# Create your views here.
def index(request):
    categories = models.Category.objects.all()
    meals = models.Meal.objects.all()
    context = {'categories': categories,
               'meals': meals}
    return render(request, 'home/index.html', context)
