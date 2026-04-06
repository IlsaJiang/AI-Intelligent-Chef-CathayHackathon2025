from rest_framework import viewsets
from .models import Dish, Allergen, Ingredient
from .serializers import DishSerializer, AllergenSerializer, IngredientSerializer
from chat.models import FAQEntry  # 引入 FAQEntry 模型
from rest_framework import serializers


# FAQEntry 的序列化器
class FAQEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQEntry
        fields = "__all__"


# 菜品 API
class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


# 过敏原 API
class AllergenViewSet(viewsets.ModelViewSet):
    queryset = Allergen.objects.all()
    serializer_class = AllergenSerializer


# 配料 API
class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


# FAQ 问答数据 API
class FAQEntryViewSet(viewsets.ModelViewSet):
    queryset = FAQEntry.objects.all()
    serializer_class = FAQEntrySerializer