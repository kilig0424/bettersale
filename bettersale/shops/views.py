from django.shortcuts import render

# Create your views here.
# views.py
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ShopType, School, Shop, SurroundingInfo
from .serializers import ShopTypeSerializer, SchoolSerializer, ShopSerializer, SurroundingInfoSerializer


class ShopTypeViewSet(viewsets.ModelViewSet):
    queryset = ShopType.objects.all()
    serializer_class = ShopTypeSerializer


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class ShopViewSet(viewsets.ModelViewSet):
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]  # 添加权限类，要求用户必须已经登录
    authentication_classes = (CsrfExemptSessionAuthentication, )  # 禁用CSRF保护

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # 获取用户的商店
            shops = Shop.objects.filter(user=user)
            return shops
        # 如果用户未登录，返回空的查询集
        return Shop.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SurroundingInfoViewSet(viewsets.ModelViewSet):
    serializer_class = SurroundingInfoSerializer
    permission_classes = [IsAuthenticated]  # 添加权限类，要求用户必须已经登录

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # 获取用户的商店
            shops = Shop.objects.filter(user=user)
            # 获取这些商店的周边信息
            surrounding_infos = SurroundingInfo.objects.filter(shop__in=shops)
            return surrounding_infos
        # 如果用户未登录，返回空的查询集
        return SurroundingInfo.objects.none()


class SchoolViewSet(viewsets.ModelViewSet):
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        shop_id = self.kwargs['shop_id']  # 从URL中获取商店ID
        return School.objects.filter(shop__id=shop_id)  # 根据商店ID过滤学校

    def create(self, request, *args, **kwargs):
        shop_id = self.kwargs['shop_id']  # 从URL中获取商店ID
        shop = Shop.objects.get(id=shop_id)  # 获取商店对象
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(shop=shop)  # 在创建学校时，将商店对象添加到学校对象中
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

