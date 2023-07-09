# serializers.py
from rest_framework import serializers, generics
from rest_framework.permissions import IsAuthenticated

from .models import ShopType, School, Shop, SurroundingInfo


class ShopTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopType
        fields = '__all__'


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        exclude = ('user',)  # 排除'user'字段

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.pop('user', None)  # 删除validated_data中的'user'字段
        shop = Shop.objects.create(user=user, **validated_data)
        return shop


class SurroundingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurroundingInfo
        fields = '__all__'



