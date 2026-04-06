from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import IdentifierTokenObtainPairView, RegisterView, MeView, SendOtpView

urlpatterns = [
    path('login/', IdentifierTokenObtainPairView.as_view(), name='auth-login'),
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('refresh/', TokenRefreshView.as_view(), name='auth-refresh'),
    path('me/', MeView.as_view(), name='auth-me'),
    path('send-otp/', SendOtpView.as_view(), name='auth-send-otp'),
]

