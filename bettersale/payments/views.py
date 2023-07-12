from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required

from users.models import User
# from users.sms import send_sms
from .models import Membership, Card
from .serializers import CardSerializer
from django.http import HttpResponse
import csv
from django.shortcuts import render
from django.http import HttpResponseRedirect
import random
import string
from django.views import View
from django.http import JsonResponse
from .models import Card


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


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


@csrf_exempt
def send_verification_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone_number = data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            return JsonResponse({'status': 'error', 'message': 'This phone number has already been bound to'
                                                               ' another account.'})
        code = random.randint(100000, 999999)  # 生成6位数的验证码
        send_sms(phone_number, str(code))
        request.session['verification_code'] = code
        request.session['phone_number'] = phone_number
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})



@login_required
@csrf_exempt
def verify_phone_number(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code')
        if int(code) == request.session.get('verification_code'):
            request.user.profile.phone_number = request.session.get('phone_number')
            request.user.profile.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid verification code.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
