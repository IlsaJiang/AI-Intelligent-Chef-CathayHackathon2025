from django.contrib import admin
from .models import Dish, Allergen, Ingredient, DishIngredient

class DishIngredientInline(admin.TabularInline):
    model = DishIngredient
    extra = 1

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('id','name_zh','name_en','calories')
    inlines = [DishIngredientInline]

@admin.register(Allergen)
class AllergenAdmin(admin.ModelAdmin):
    list_display = ('code','name_zh','name_en')

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name_zh','name_en')
