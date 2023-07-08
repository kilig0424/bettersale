from django.contrib import admin
from .models import User, Membership


# 定义Admin界面的展示方式
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_number','is_active', 'is_staff', 'date_joined', 'display_name']
    list_filter = ['is_active', 'is_staff']
    search_fields = ['username', 'email']


class MembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_date', 'end_date', 'membership_type']
    list_filter = ['end_date', 'membership_type']
    search_fields = ['user', 'membership_type']


# 注册模型到Admin
admin.site.register(User, UserAdmin)
admin.site.register(Membership, MembershipAdmin)