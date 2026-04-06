from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from menu.views import DishViewSet, AllergenViewSet, IngredientViewSet, FAQEntryViewSet
from surveys.views import SurveyResponseViewSet, LeftoverSubmissionViewSet, PeriodicFeedbackViewSet
from chat.views import chat_with_chef
from integrations.views import choose_meal_bridge

router = routers.DefaultRouter()
router.register(r'dishes', DishViewSet)
router.register(r'allergens', AllergenViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'faqs', FAQEntryViewSet)
router.register(r'survey', SurveyResponseViewSet)
router.register(r'leftover', LeftoverSubmissionViewSet)
router.register(r'periodic-feedback', PeriodicFeedbackViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/', include(router.urls)),
    path('api/auth/', include('accounts.urls')),
    path('api/chat/', chat_with_chef),
    path('api/integrations/cx/choose-meal/', choose_meal_bridge),
    path("api/chef/", include("ai_chef.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)