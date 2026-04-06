from rest_framework import serializers
from .models import Dish, Ingredient, Allergen, DishIngredient

class AllergenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergen
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    allergens = AllergenSerializer(many=True, read_only=True)
    class Meta:
        model = Ingredient
        fields = '__all__'

class DishIngredientNestedSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    class Meta:
        model = DishIngredient
        fields = ('ingredient','amount','unit')

class DishSerializer(serializers.ModelSerializer):
    allergens = AllergenSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = ('id','name_zh','name_zh_hk','name_en','desc_zh','desc_zh_hk','desc_en','calories','protein_g','fat_g','carbs_g','hero_image','video_url','allergens','ingredients')

    def get_ingredients(self, obj):
        links = DishIngredient.objects.filter(dish=obj).select_related('ingredient')
        return DishIngredientNestedSerializer(links, many=True).data