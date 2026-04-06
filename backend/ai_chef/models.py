from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AIChefChatMessage(models.Model):
    """AI厨师聊天消息记录"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()  # 用户消息
    reply = models.TextField()  # AI回复
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "AI Chef Chat Message"
        verbose_name_plural = "AI Chef Chat Messages"
    
    def __str__(self):
        return f"{self.user} - {self.created_at}"

