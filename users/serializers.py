from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["telegram_id", "name", "phone_number", "role", "is_staff"]
        extra_kwargs = {
            "role": {"default": "user"},
            "is_staff": {"default": False}
        }




class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "telegram_id",
            "name",
            "phone_number",
            "role",
            "created_at",
        ]