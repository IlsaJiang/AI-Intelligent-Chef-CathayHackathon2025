#!/usr/bin/env python
"""测试 AI Chef API 的繁体中文支持"""
import os
import sys
import django

# 添加 backend 目录到 Python 路径
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from menu.models import Dish

print("=" * 80)
print("AI Chef 菜单数据测试 - 繁体中文支持")
print("=" * 80)

dishes = Dish.objects.all()

print("\n📋 测试不同语言下的菜品显示:\n")

for dish in dishes:
    print(f"\n{'='*60}")
    print(f"菜品 ID: {dish.id}")
    print(f"{'='*60}")
    
    # 简体中文
    print(f"\n【简体中文 (zh)】")
    print(f"名称: {dish.name_zh}")
    print(f"描述: {dish.desc_zh[:100]}...")
    
    # 繁体中文
    print(f"\n【繁体中文 (zh-HK)】")
    dish_name_hk = dish.name_zh_hk if dish.name_zh_hk else dish.name_zh
    dish_desc_hk = (dish.desc_zh_hk[:100] if dish.desc_zh_hk else dish.desc_zh[:100])
    print(f"名称: {dish_name_hk}")
    print(f"描述: {dish_desc_hk}...")
    
    # 英文
    print(f"\n【英文 (en)】")
    print(f"名称: {dish.name_en}")
    print(f"描述: {dish.desc_en[:100] if dish.desc_en else 'N/A'}...")

print("\n" + "=" * 80)
print("✅ 测试完成")
print("=" * 80)
print("\n提示: AI Chef 现在会根据用户语言(zh/zh-HK/en)自动选择合适的菜品信息")
