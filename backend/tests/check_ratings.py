#!/usr/bin/env python
"""检查问卷评分数据"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from surveys.models import SurveyResponse

print("=" * 60)
print("检查问卷评分数据")
print("=" * 60)

surveys = SurveyResponse.objects.all()
print(f"\n问卷总数: {surveys.count()}")

if surveys.exists():
    print("\n所有问卷的评分:")
    print(f"{'ID':<5} {'菜品':<20} {'评分':<10} {'评分类型':<15}")
    print("-" * 60)
    
    for survey in surveys:
        dish_name = survey.dish.name_zh if survey.dish else 'N/A'
        rating_type = type(survey.rating).__name__
        print(f"{survey.id:<5} {dish_name:<20} {survey.rating:<10} {rating_type:<15}")
    
    # 统计评分分布
    print("\n评分分布:")
    for i in range(6):
        count = surveys.filter(rating=i).count()
        if count > 0:
            print(f"  {i} 星: {count} 条")
    
    # 检查是否有异常评分
    invalid_ratings = surveys.exclude(rating__in=[0, 1, 2, 3, 4, 5])
    if invalid_ratings.exists():
        print("\n⚠️  发现异常评分:")
        for survey in invalid_ratings:
            print(f"  ID: {survey.id}, 评分: {survey.rating}")
else:
    print("\n数据库中没有问卷数据")

print("\n" + "=" * 60)
