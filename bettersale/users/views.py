import string
import random
from datetime import timedelta
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import generics, viewsets
import json
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from bettersale.settings import DEFAULT_FROM_EMAIL
from payments.models import Card
from .models import User, UserSession
from .serializers import UserSerializer, MembershipSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserSession
from rest_framework.authentication import SessionAuthentication
import re
from django.utils import timezone
from django.core.mail import send_mail
from .models import EmailVerificationCode
from django.core.mail import send_mail
from django.views import View
from .models import Membership


# RegisterView，继承自APIView
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    authentication_classes = [SessionAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# UserViewSet，继承自ModelViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# login_view，一个函数视图
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        device_type = data['device_type']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # 删除旧的 session
            UserSession.objects.filter(user=user, device_type=device_type).delete()
            # 创建新的 session
            UserSession.objects.create(user=user, session_id=request.session.session_key, device_type=device_type)
            return JsonResponse({'status': 'success', 'user_id': user.id})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid username or password'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# 退出登录
@csrf_exempt
def logout_view(request):
    if request.user.is_authenticated:  # 检查用户是否已经登录
        user = request.user
        device_type = request.POST.get('device_type')
        UserSession.objects.filter(user=user, device_type=device_type).delete()
    logout(request)
    return JsonResponse({'status': 'success'})


@method_decorator(csrf_exempt, name='dispatch')
class UserDetail(APIView):
    @csrf_exempt
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    @csrf_exempt
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        if 'display_name' in data:
            user.display_name = data['display_name']
        if 'security_question' in data:
            user.security_question = data['security_question']
        if 'security_answer' in data:
            user.security_answer = data['security_answer']
        user.save()
        return JsonResponse({'status': 'success'})


@csrf_exempt
def change_password(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        if not user.check_password(old_password):
            return JsonResponse({'status': 'error', 'message': 'Old password is incorrect'}, status=400)
        if len(new_password) < 8:
            return JsonResponse({'status': 'error', 'message': 'Password needs to be at least 8 characters.'}, status=400)
        if not re.search('[a-z]', new_password) or not re.search('[A-Z]', new_password):
            return JsonResponse({'status': 'error',
                                 'message': 'Password needs to include both lowercase and uppercase letters.'}, status=400)
        if not re.search('[0-9]', new_password):
            return JsonResponse({'status': 'error', 'message': 'Password needs to include a number.'}, status=400)
        user.set_password(new_password)
        user.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class EmailVerification(APIView):
    #  生成验证码，保存到数据库，并发送到用户的邮箱
    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
        data = json.loads(request.body)
        email = data.get('email')
        if email is None:
            return JsonResponse({'status': 'error', 'message': 'Email is required'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email already in use'}, status=400)
        code = random.randint(100000, 999999)
        EmailVerificationCode.objects.create(code=code, email=email, expires_at=timezone.now() + timedelta(minutes=10))
        send_mail(
            'Your verification code',
            'Your verification code is: ' + str(code),
            'kilig@bettersale.cn',
            [email],
            fail_silently=False,
        )
        return JsonResponse({'status': 'success'})

    # 处理PUT请求，验证用户输入的验证码是否正确。
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
        email = request.POST.get('email')
        code = request.POST.get('code')
        try:
            verification_code = EmailVerificationCode.objects.get(code=code, email=email)
        except EmailVerificationCode.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid verification code'}, status=400)
        if timezone.now() > verification_code.expires_at:
            return JsonResponse({'status': 'error', 'message': 'Verification code expired'}, status=400)
        user.email = email
        user.save()
        verification_code.delete()
        return JsonResponse({'status': 'success'})


# 获取用户的会员状态
class MembershipStatusView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            membership = Membership.objects.get(user=user)
            if membership.is_active():
                return JsonResponse({'status': 'active', 'end_date': membership.end_date})
            else:
                return JsonResponse({'status': 'inactive'})
        else:
            return JsonResponse({'status': 'not logged in'})


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


@method_decorator(csrf_exempt, name='dispatch')
class ActivateCardView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'You need to log in to activate a membership card.'})

        data = json.loads(request.body)
        card_number = data.get('card_number')
        password = data.get('password')
        print(card_number)
        print(password)

        try:
            card = Card.objects.get(card_number=card_number, password=password)
            if card.is_active:
                return JsonResponse({'status': 'error', 'message': 'This card has already been activated.'})
            card.activate(request.user)
            return JsonResponse({'status': 'success', 'message': 'Membership activated successfully.'})
        except Card.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid card number or password.'})



