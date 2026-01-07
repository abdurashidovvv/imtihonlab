from rest_framework import serializers
from .models import User

class TelegramAuthSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
