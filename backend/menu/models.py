from django.db import models

class Allergen(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name_zh = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)

    def __str__(self):
        return self.name_zh

class Ingredient(models.Model):
    name_zh = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    allergens = models.ManyToManyField(Allergen, blank=True)

    def __str__(self):
        return self.name_zh

class Dish(models.Model):
    name_zh = models.CharField(max_length=200)
    name_zh_hk = models.CharField(max_length=200, blank=True)  # 繁体中文名称
    name_en = models.CharField(max_length=200)
    desc_zh = models.TextField(blank=True)
    desc_zh_hk = models.TextField(blank=True)  # 繁体中文描述
    desc_en = models.TextField(blank=True)
    calories = models.IntegerField(null=True, blank=True)  # kcal
    protein_g = models.FloatField(null=True, blank=True)
    fat_g = models.FloatField(null=True, blank=True)
    carbs_g = models.FloatField(null=True, blank=True)
    hero_image = models.ImageField(upload_to='dishes/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    allergens = models.ManyToManyField(Allergen, blank=True, related_name='dishes')

    def __str__(self):
        return self.name_zh

class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=20, blank=True)