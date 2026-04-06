from django.db import models
from django.contrib.auth import get_user_model
from menu.models import Dish
User = get_user_model()

LEFTOVER_CHOICES = ((0,'None'),(1,'<25%'),(2,'25-50%'),(3,'50-75%'),(4,'>75%'))

# 剩余原因选项
LEFTOVER_REASON_CHOICES = (
    (0, '未选择'),
    (1, '口味问题'),  # 不合口味、太辣、太甜等
    (2, '分量问题'),  # 分量太大、分量不足
    (3, '个人原因'),  # 已饱、赶时间
    (4, '菜品质量'),  # 有异物、不新鲜
)

# 反馈状态选项
FEEDBACK_STATUS_CHOICES = (
    (0, '已收到'),
    (1, '已采纳'),
    (2, '已拒绝'),
)

# 细化评分选项
TASTE_CHOICES = (
    (0, '未选择'),
    (1, '偏咸'),
    (2, '偏淡'),
    (3, '适中'),
)

TEXTURE_CHOICES = (
    (0, '未选择'),
    (1, '火候过老'),
    (2, '火候过嫩'),
    (3, '适中'),
)

QUANTITY_CHOICES = (
    (0, '未选择'),
    (1, '分量太大'),
    (2, '分量适中'),
    (3, '分量不足'),
)

# 照片类型选项
PHOTO_TYPE_CHOICES = (
    (0, '菜品照片'),
    (1, '剩餐照片'),
)

class SurveyResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField(default=0)  # 1-5
    
    # 细化评分
    taste_rating = models.IntegerField(choices=TASTE_CHOICES, default=0)  # 口味评分
    texture_rating = models.IntegerField(choices=TEXTURE_CHOICES, default=0)  # 口感评分
    quantity_rating = models.IntegerField(choices=QUANTITY_CHOICES, default=0)  # 分量评分
    
    leftover_level = models.IntegerField(choices=LEFTOVER_CHOICES, default=0)
    leftover_reason = models.IntegerField(choices=LEFTOVER_REASON_CHOICES, default=0)  # 剩余原因（非必选）
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 反馈状态追踪
    status = models.IntegerField(choices=FEEDBACK_STATUS_CHOICES, default=0)
    chef_response = models.TextField(blank=True)  # 厨师长回复
    
    # 里数相关字段
    miles_awarded = models.BooleanField(default=False)
    awarded_at = models.DateTimeField(null=True, blank=True)

class LeftoverSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, blank=True)
    photo = models.ImageField(upload_to='leftovers/')
    leftover_percent = models.IntegerField(default=0)  # 0-100
    photo_type = models.IntegerField(choices=PHOTO_TYPE_CHOICES, default=0)  # 照片类型
    created_at = models.DateTimeField(auto_now_add=True)

# 周期性反馈模型
class PeriodicFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    question = models.CharField(max_length=255)  # 问题
    answer = models.TextField()  # 回答
    miles_awarded = models.BooleanField(default=False)  # 是否已发放里数
    created_at = models.DateTimeField(auto_now_add=True)

# 添加里数记录模型
class PointTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    survey = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE, related_name='point_transactions', null=True, blank=True)
    periodic_feedback = models.ForeignKey(PeriodicFeedback, on_delete=models.CASCADE, related_name='point_transactions', null=True, blank=True)
    miles = models.IntegerField(default=0)  # 发放的里数数量
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)  # 积分发放说明

# 添加里数记录模型
class MilesTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    miles = models.IntegerField(default=0)  # 发放的里数数量
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)  # 里数发放说明
    reason = models.CharField(max_length=50, blank=True)  # 奖励原因，如 'ai_chef_chat'
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Miles Transaction"
        verbose_name_plural = "Miles Transactions"
    
    def __str__(self):
        return f"{self.user} - {self.miles} miles ({self.reason})"
