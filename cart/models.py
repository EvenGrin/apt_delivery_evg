from django.contrib.auth.models import User
from django.db import models

from home.models import Meal


# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, default=None, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=None)

