from datetime import datetime
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import User


# 自定义的UserManager，继承自BaseUserManager
class UserManager(BaseUserManager):
    # 添加get_by_natural_key方法，用于通过自然键获取用户
    def get_by_natural_key(self, username):
        # 使用get方法从数据库中获取用户名为username的用户
        return self.get(username=username)

    # 创建并保存一个超级用户
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('超级用户必须有is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('超级用户必须有is_superuser=True.')
        return self.create_user(username, email, password, **extra_fields)

    # 创建并保存一个用户
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('必须输入用户名')
        if not email:
            raise ValueError('必须输入邮箱')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


# User模型，继承自AbstractBaseUser和PermissionsMixin
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, verbose_name='用户名')
    email = models.EmailField(unique=False, blank=True, verbose_name='邮箱地址')
    is_active = models.BooleanField(default=True, verbose_name='是否活跃')
    is_staff = models.BooleanField(default=False, verbose_name='是否可以登录djaingo后台')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    display_name = models.CharField(max_length=255, blank=True, verbose_name='昵称')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='手机号码')
    security_question = models.CharField(max_length=255,blank=True, verbose_name='安全问题')
    security_answer = models.CharField(max_length=255,blank=True, verbose_name='安全问题答案')

    # 使用自定义的UserManager
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


# UserSession模型，用于存储用户的登录状态
class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=40)
    device_type = models.CharField(max_length=20)
    login_time = models.DateTimeField(auto_now_add=True)


# 用于存储邮箱验证的验证码
class EmailVerificationCode(models.Model):
    code = models.CharField(max_length=6)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()


# 会员模型
class Membership(models.Model):
    MEMBERSHIP_CHOICES = (
        ('non_member', '非会员'),
        ('ordinary_member', '普通会员'),
        ('member_type_1', '会员种类1'),
        ('member_type_2', '会员种类2'),
        ('member_type_3', '会员种类3'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True, blank=True)  # 会员开始日期
    end_date = models.DateTimeField(null=True, blank=True)  # 会员结束日期
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES, default='non_member')  # 会员类型

    def is_active(self):
        # 判断会员是否在有效期内
        now = timezone.now()
        return self.start_date <= now <= self.end_date

