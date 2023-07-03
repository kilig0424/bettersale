import re

from django.db import IntegrityError
from rest_framework import serializers
from .models import User, Membership


# UserSerializer，继承自ModelSerializer
class UserSerializer(serializers.ModelSerializer):
    # password字段是只写的，不会被序列化
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'is_active',
                  'is_staff', 'date_joined', 'display_name', 'password', 'security_question']

    # 验证password字段的方法
    @staticmethod
    def validate_password(value):
        if len(value) < 8:
            raise serializers.ValidationError("密码需要至少8位数。")
        if not re.search('[a-z]', value) or not re.search('[A-Z]', value):
            raise serializers.ValidationError("密码需要包含大小写。")
        if not re.search('[0-9]', value):
            raise serializers.ValidationError("密码必须包含数字。")
        return value

    # 创建User实例的方法
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        try:
            user.save()
        except IntegrityError:
            raise serializers.ValidationError("用户名已存在")
        return user


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['user', 'start_date', 'end_date', 'membership_type']
