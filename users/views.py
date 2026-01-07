from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import TelegramAuthSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class TelegramAuthView(APIView):

    @staticmethod
    def post(request):
        serializer = TelegramAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        telegram_id = data['telegram_id']
        name = data.get('name', '')

        # User yaratish yoki topish
        user, created = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={"name": name}
        )

        # JWT token
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "telegram_id": user.telegram_id,
                "name": user.name,
                "role": user.role
            }
        }, status=status.HTTP_200_OK)