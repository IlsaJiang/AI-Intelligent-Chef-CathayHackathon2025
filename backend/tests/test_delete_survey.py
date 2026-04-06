#!/usr/bin/env python
"""测试删除问卷的脚本"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from surveys.models import SurveyResponse, PointTransaction
from menu.models import Dish

print("=" * 60)
print("检查数据库状态")
print("=" * 60)

# 1. 检查问卷数量
surveys = SurveyResponse.objects.all()
print(f"\n当前问卷总数: {surveys.count()}")

if surveys.exists():
    print("\n前 5 条问卷:")
    for survey in surveys[:5]:
        print(f"  ID: {survey.id}, 菜品: {survey.dish.name_zh if survey.dish else 'N/A'}, 评分: {survey.rating}")
        
        # 检查是否有关联的积分交易
        transactions = PointTransaction.objects.filter(survey=survey)
        if transactions.exists():
            print(f"    └─ 关联积分交易: {transactions.count()} 条")
            for trans in transactions:
                print(f"       - ID: {trans.id}, 积分: {trans.miles}, 描述: {trans.description}")

# 2. 测试删除功能
print("\n" + "=" * 60)
print("测试删除功能")
print("=" * 60)

if surveys.count() > 0:
    test_survey = surveys.first()
    print(f"\n准备删除问卷 ID: {test_survey.id}")
    
    # 检查关联数据
    related_transactions = PointTransaction.objects.filter(survey=test_survey).count()
    print(f"关联的积分交易数: {related_transactions}")
    
    try:
        # 尝试删除
        test_id = test_survey.id
        test_survey.delete()
        print(f"✅ 成功删除问卷 ID: {test_id}")
        
        # 验证级联删除
        remaining_transactions = PointTransaction.objects.filter(survey_id=test_id).count()
        print(f"删除后剩余的关联积分交易: {remaining_transactions}")
        
        if remaining_transactions == 0:
            print("✅ 级联删除成功")
        else:
            print("⚠️  警告: 仍有关联的积分交易未被删除")
            
    except Exception as e:
        print(f"❌ 删除失败: {e}")
        import traceback
        traceback.print_exc()
else:
    print("\n数据库中没有问卷数据，无法测试删除")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
