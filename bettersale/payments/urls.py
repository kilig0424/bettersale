from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views
from .views import CardViewSet, ActivateCardView

router = DefaultRouter()
router.register(r'cards', CardViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('activate_card/', ActivateCardView.as_view(), name='activate_card'),

]
