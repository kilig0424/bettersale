from django.contrib import admin
from .models import ShopType, School, Shop, SurroundingInfo


# 注册ShopType模型
@admin.register(ShopType)
class ShopTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']  # 在admin界面中显示的字段
    search_fields = ['name']  # 添加搜索字段
    ordering = ['name']  # 设置默认排序字段


# 注册School模型
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'student_count', 'school_type', 'walk_type','shop']
    search_fields = ['name']
    ordering = ['name']


# 注册Shop模型
@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     form.base_fields['nearby_schools'].initial = None
    #     return form

    list_display = ['name', 'city', 'district', 'shop_type', 'scale', 'community_type', 'dominant_shop_type',
                    'average_house_price', 'user']
    search_fields = ['name']
    ordering = ['name']


# 注册SurroundingInfo模型
@admin.register(SurroundingInfo)
class SurroundingInfoAdmin(admin.ModelAdmin):
    list_display = ['info_name', 'info_type', 'info_address', 'distance']
    search_fields = ['info_name']
    ordering = ['info_name']
