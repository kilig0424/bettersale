from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import UserViewSet, EmailVerification,
from .views import RegisterView, login_view, logout_view, UserDetail, change_password, MembershipStatusView, UserViewSet

# 创建一个DefaultRouter实例
router = DefaultRouter()
# 将UserViewSet注册到router
router.register(r'users', UserViewSet)

# 定义URL模式
urlpatterns = [
    # 包含router的URL模式
    path('', include(router.urls)),
    # 注册视图的URL模式
    path('register/', RegisterView.as_view(), name='user_register'),
    # 登录视图的URL模式
    path('login/', login_view, name='login'),
    # 退出登录
    path('logout/', logout_view, name='logout'),
    # 获取用户信息
    path('user/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    # 修改密码
    path('user/<int:pk>/change_password/', change_password, name='change_password'),
    # 验证绑定邮箱
    # path('user/<int:pk>/verify_email/', EmailVerification.as_view(), name='verify_email'),
    # 判断会员状态
    path('membership_status/', MembershipStatusView.as_view(), name='membership_status'),

]
