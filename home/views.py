from django.shortcuts import render

from home import models


# Create your views here.
def index(request):
    categories = models.Category.objects.all()
    context = {'categories': categories}
    return render(request, 'home/index.html', context)