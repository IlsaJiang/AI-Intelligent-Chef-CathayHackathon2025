from django.urls import path
from .views import AIChefChatView

urlpatterns = [
    path("chat/", AIChefChatView.as_view(), name="ai_chef_chat"),
]
