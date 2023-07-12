from rest_framework import serializers

from payments.models import Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['card_number', 'password', 'is_active', 'days', 'create_time']