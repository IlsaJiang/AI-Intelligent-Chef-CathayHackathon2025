from django.db import models
from django.contrib.auth import get_user_model
from menu.models import Dish
User = get_user_model()

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10)  # user/assistant/system
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class FAQEntry(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='faqs')
    lang = models.CharField(max_length=5, choices=[('zh','Chinese'),('en','English')])
    question = models.CharField(max_length=255)
    answer = models.TextField()
