from django.db import models
from django.contrib.auth import get_user_model
from menu.models import Dish
User = get_user_model()

class MealSelection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True)
    flight_no = models.CharField(max_length=20)
    flight_date = models.DateField()
    status = models.CharField(max_length=20, default='pending')
    external_reference = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
