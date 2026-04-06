# dish.py
from menu.models import Dish, Ingredient, Allergen, DishIngredient

# 清除已存在的同名菜品及相关数据
Dish.objects.filter(name_zh='八宝红鲟饭').delete()

# 创建过敏原
shellfish_allergen = Allergen.objects.create(
    code='shellfish',
    name_zh='甲壳类动物',
    name_en='Shellfish'
)

peanut_allergen = Allergen.objects.create(
    code='peanuts',
    name_zh='花生',
    name_en='Peanuts'
)

soy_allergen = Allergen.objects.create(
    code='soy',
    name_zh='大豆',
    name_en='Soy'
)

wheat_allergen = Allergen.objects.create(
    code='wheat',
    name_zh='小麦',
    name_en='Wheat'
)

# 创建配料
ingredients_data = [
    {'name_zh': '糯米', 'name_en': 'Glutinous Rice'},
    {'name_zh': '红鲟（青蟹）', 'name_en': 'Red Crab (Mud Crab)'},
    {'name_zh': '火腿肠', 'name_en': 'Ham Sausage'},
    {'name_zh': '鸭肉', 'name_en': 'Duck Meat'},
    {'name_zh': '猪肚', 'name_en': 'Pork Stomach'},
    {'name_zh': '鸭肫', 'name_en': 'Duck Gizzard'},
    {'name_zh': '虾米', 'name_en': 'Dried Shrimp'},
    {'name_zh': '竹笋', 'name_en': 'Bamboo Shoots'},
    {'name_zh': '炸花生仁', 'name_en': 'Fried Peanuts'},
    {'name_zh': '鲜香菇', 'name_en': 'Fresh Shiitake Mushrooms'},
    {'name_zh': '大葱', 'name_en': 'Scallion'},
    {'name_zh': '姜', 'name_en': 'Ginger'},
    {'name_zh': '料酒', 'name_en': 'Cooking Wine'},
    {'name_zh': '白酱油', 'name_en': 'Light Soy Sauce'},
    {'name_zh': '胡椒', 'name_en': 'Pepper'},
    {'name_zh': '味精', 'name_en': 'MSG'},
    {'name_zh': '猪油', 'name_en': 'Lard'},
]

ingredients = []
for data in ingredients_data:
    ingredient = Ingredient.objects.create(**data)
    ingredients.append(ingredient)

# 为配料关联过敏原
ingredients[1].allergens.add(shellfish_allergen)  # 红鲟（青蟹）
ingredients[6].allergens.add(shellfish_allergen)  # 虾米
ingredients[8].allergens.add(peanut_allergen)    # 炸花生仁
ingredients[13].allergens.add(soy_allergen, wheat_allergen)  # 白酱油

# 创建菜品
xunweizhonghua_dish = Dish.objects.create(
    name_zh='八宝红鲟饭',
    name_en='Eight Treasures Red Crab Rice',
    desc_zh='福建福州的传统名点，属于闽菜系福州菜。以红鲟（青蟹）和糯米为主料，搭配火腿、鸭肉、猪肚、鸭肫、虾米、竹笋、花生仁、香菇等八种辅料蒸制而成，味道咸鲜软糯，营养丰富，寓意美好。',
    desc_en='A traditional delicacy from Fuzhou, Fujian, belonging to the Min cuisine. Made with red crab (mud crab) and glutinous rice as main ingredients, accompanied by eight supplementary ingredients including ham, duck meat, pork stomach, duck gizzard, dried shrimp, bamboo shoots, peanuts, and mushrooms, steamed to perfection. It has a savory and soft texture, rich in nutrition, and carries auspicious meanings.',
    calories=1414,
    protein_g=65.2,
    fat_g=42.8,
    carbs_g=178.3
)

# 关联过敏原到菜品
xunweizhonghua_dish.allergens.add(shellfish_allergen, peanut_allergen, soy_allergen, wheat_allergen)

# 关联配料到菜品
dish_ingredients_data = [
    (ingredients[0], 125, '克'),   # 糯米
    (ingredients[1], 750, '克'),   # 红鲟（青蟹）
    (ingredients[2], 10, '克'),    # 火腿肠
    (ingredients[3], 10, '克'),    # 鸭肉
    (ingredients[4], 10, '克'),    # 猪肚
    (ingredients[5], 10, '克'),    # 鸭肫
    (ingredients[6], 5, '克'),     # 虾米
    (ingredients[7], 10, '克'),    # 竹笋
    (ingredients[8], 5, '克'),     # 炸花生仁
    (ingredients[9], 5, '克'),     # 鲜香菇
    (ingredients[10], 8, '克'),    # 大葱
    (ingredients[11], 5, '克'),    # 姜
    (ingredients[12], 6, '克'),    # 料酒
    (ingredients[13], 5, '克'),    # 白酱油
    (ingredients[14], 1, '克'),    # 胡椒
    (ingredients[15], 1, '克'),    # 味精
    (ingredients[16], 30, '克'),   # 猪油
]

for ingredient, amount, unit in dish_ingredients_data:
    DishIngredient.objects.create(
        dish=xunweizhonghua_dish,
        ingredient=ingredient,
        amount=amount,
        unit=unit
    )

print("搞tmd定！")
print(f"菜品ID: {xunweizhonghua_dish.id}")
print(f"配料数量: {len(dish_ingredients_data)}")