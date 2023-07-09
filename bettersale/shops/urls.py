# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShopTypeViewSet, SchoolViewSet, ShopViewSet, SurroundingInfoViewSet


router = DefaultRouter()
router.register(r'shoptypes', ShopTypeViewSet)
router.register(r'schools', SchoolViewSet, basename='school')
router.register(r'shops', ShopViewSet, basename='shop')
router.register(r'surroundinginfos', SurroundingInfoViewSet, basename='surroundinginfo')
router.register(r'shops/(?P<shop_id>\d+)/schools', SchoolViewSet, basename='shop-schools')


urlpatterns = [
    path('', include(router.urls)),
]
