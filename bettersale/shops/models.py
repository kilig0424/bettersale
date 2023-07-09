from django.db import models
from users.models import User
from django.conf import settings
# Create your models here.


# ShopType模型用于存储不同类型的商店
class ShopType(models.Model):
    # 商店类型的名称
    name = models.CharField(max_length=50)
    # 自关联字段，用于表示上一级类型
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


# School模型用于存储学校详情
class School(models.Model):
    SCHOOL_TYPES = [
        ('kindergarten ', '幼儿园'),
        ('primary', '小学'),
        ('secondary', '中学'),
        ('university', '大学'),
        ('trade', '职业学校'),
        ('others', '其他'),
    ]
    STUDENT_COUNTS = [
        ('1000', '1000以内'),
        ('2000', '1000-2000'),
        ('3000', '3000以上'),
    ]
    WALK_TYPES = [
        ('walk', '走读'),
        ('live', '住校'),
        ('mix', '混合'),
    ]
    # 链接到与学校关联的商店，在Django中，当你在一个模型中定义了一个ManyToManyField，
    # Django会自动在另一个模型中创建一个反向关系。
    # shop = models.ManyToManyField('Shop')
    # 学校的名称
    name = models.CharField(max_length=100, verbose_name='学校名字')
    # 学校的学生人数
    student_count = models.CharField(max_length=20, choices=STUDENT_COUNTS, verbose_name='学生人数')
    # 学校的类型
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPES, verbose_name='学校类型')
    # 学校的上学类型，走读住读还是混合
    walk_type = models.CharField(max_length=20, choices=WALK_TYPES, verbose_name='走读住读')
    # 学校对应的店铺
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, verbose_name='店铺', blank=True)

    def __str__(self):
        return self.name


# Shop模型用于存储商店详情
class Shop(models.Model):
    SCALES = [
        ('10', '10万以内'),
        ('30', '10-30万'),
        ('100', '30-100万'),
        ('500', '100-500万'),
        ('1000', '500万以上')
    ]
    DOMINANT_SHOP_TYPES = [
        ('M1001', '零售'),
        ('M1002', '餐饮'),
        ('M1003', '休闲娱乐'),
        ('M1004', '服务行业'),
        ('M1005', '教育培训'),
        ('M1006', '医疗保健'),
        ('M1007', '文化艺术'),
        ('M1009', '服饰'),
        ('M1008', '其他'),
    ]
    COMMUNITY_TYPES = [
        ('T1001', '社区'),
        ('T1002', '商圈'),
        ('T1003', '景区'),
        ('T1004', '办公园区'),
        ('T1005', '其他'),
    ]
    AVERAGE_HOUSE_PRICE_CHOICES = [
        ('5000', '5000以内'),
        ('10000', '5001-10000'),
        ('15000', '10001-15000'),
        ('20000', '15001-20000'),
        ('25000', '20001-25000'),
        ('30000', '25001-30000'),
        ('30001', '30000以上'),
    ]
    # 链接到拥有该商店的用户
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 商店的名称
    name = models.CharField(max_length=100, verbose_name='店铺名称')
    # 商店的地址
    # 省
    province = models.CharField(max_length=100, verbose_name='省(直辖市填写市名)')
    # 城市
    city = models.CharField(max_length=100, verbose_name='市')
    # 区县
    district = models.CharField(max_length=100, verbose_name='区/县')
    # 街道
    street = models.CharField(max_length=100, verbose_name='街道')
    # 详细地址
    detailed_address = models.CharField(max_length=200, verbose_name='详细地址')
    # 商店的类型，链接到ShopType模型
    shop_type = models.ForeignKey(ShopType, on_delete=models.CASCADE, verbose_name='店铺类型')
    # 商店的规模，用户自行选择一个规模
    scale = models.CharField(max_length=20, choices=SCALES, verbose_name='店铺规模')
    # 商店所在社区的类型
    community_type = models.CharField(max_length=20, choices=COMMUNITY_TYPES, verbose_name='店铺环境')
    # 该区域主导的商店类型
    dominant_shop_type = models.CharField(max_length=50, choices=DOMINANT_SHOP_TYPES, verbose_name='周边主要类型')
    # 该区域的平均房价
    average_house_price = models.CharField(max_length=5, choices=AVERAGE_HOUSE_PRICE_CHOICES, verbose_name='周围平均房价')
    # 该商店周围的学校
    # nearby_schools = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='周围学校', blank=True)

    def __str__(self):
        return self.name


class SurroundingInfo(models.Model):
    # 用户在用户填写地址之后，获取周边的信息，从腾讯位置服务获取到周边信息后，你可以将这些信息存储在这个模型中
    # 店铺（与Shop模型建立外键关系）
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="商店")
    # 信息类型（例如，餐馆、商店、学校等）
    info_type = models.CharField(max_length=100, verbose_name="类型")
    # 信息名称
    info_name = models.CharField(max_length=100, verbose_name="名称")
    # 信息地址
    info_address = models.CharField(max_length=200, verbose_name="地址")
    # 距离
    distance = models.FloatField(verbose_name="距离")











