#!/usr/bin/env python
"""验证菜品的繁体中文数据"""
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
print("菜品繁体中文数据验证")
print("=" * 80)

dishes = Dish.objects.all()
for dish in dishes:
    print(f"\n菜品 ID: {dish.id}")
    print(f"简体中文名: {dish.name_zh}")
    print(f"繁体中文名: {dish.name_zh_hk or '(未设置)'}")
    print(f"英文名: {dish.name_en}")
    print("-" * 80)

print("\n✅ 验证完成")
