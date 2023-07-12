import random
import string
from django.urls import path
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Card


class CardAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'password', 'days', 'is_active', 'create_time')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generate_form/', self.admin_site.admin_view(self.generate_form), name='generate_form'),
            path('generate/', self.admin_site.admin_view(self.generate_cards), name='generate'),
        ]
        return custom_urls + urls

    def generate_form(self, request):
        return render(request, 'payments/generate_form.html')

    def generate_cards(self, request):
        days = int(request.POST.get('days', 30))
        count = int(request.POST.get('count', 100))

        for _ in range(count):
            card_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
            password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
            Card.objects.create(card_number=card_number, password=password, days=days)

        return HttpResponseRedirect("../")


admin.site.register(Card, CardAdmin)
