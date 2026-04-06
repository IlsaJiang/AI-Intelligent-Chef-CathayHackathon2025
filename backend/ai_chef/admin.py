from django.contrib import admin
from .models import AIChefChatMessage


@admin.register(AIChefChatMessage)
class AIChefChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'message', 'reply']
    readonly_fields = ['created_at']

