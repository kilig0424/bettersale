# payments/models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from users.models import Membership


class Card(models.Model):
    CARD_DAYS_CHOICES = [
        (7, '7 days'),
        (30, '30 days'),
        (60, '60 days'),
        (90, '90 days'),
        (180, '180 days'),
        (360, '360 days'),
    ]

    card_number = models.CharField(max_length=20)  # 卡号
    password = models.CharField(max_length=20)  # 密码
    is_active = models.BooleanField(default=False)  # 卡是否已经被激活
    days = models.IntegerField(choices=CARD_DAYS_CHOICES, default=30)  # 卡可以增加的会员天数
    create_time = models.DateTimeField(auto_now_add=True)  # 卡的创建时间

    def activate(self, user):
        # 激活卡，为用户增加会员时间
        if self.is_active:
            raise Exception('This card has already been activated.')

        # 获取用户的会员资格，如果不存在则创建
        membership, created = Membership.objects.get_or_create(user=user)

        # 如果是新创建的会员资格，或者会员资格已经过期，那么开始日期就是现在
        if created or membership.end_date is None or membership.end_date < timezone.now():
            membership.start_date = timezone.now()

        # 如果会员资格没有过期，那么结束日期就是原来的结束日期加上卡提供的天数
        # 如果会员资格已经过期，那么结束日期就是现在加上卡提供的天数
        membership.end_date = max(membership.end_date if membership.end_date else timezone.now(),
                                  timezone.now()) + timedelta(days=self.days)

        # 将会员类型设置为普通会员
        membership.membership_type = 'ordinary_member'

        # 保存会员资格的修改
        membership.save()

        # 将卡标记为已激活
        self.is_active = True
        self.save()
