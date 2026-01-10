from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserRegisterSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from .serializers import UserListSerializer

class UserRegisterView(APIView):

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        telegram_id = data['telegram_id']
        name = data['name']
        phone_number = data['phone_number']
        role = data.get("role", "user")
        is_staff = data.get("is_staff", False)

        # User yaratish (POST dan is_staff va role olinadi)
        user, created = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                "name": name,
                "phone_number": phone_number,
                "role": role,
                "is_staff": is_staff
            }
        )

        # Agar user allaqachon bo‘lsa, ma’lumotlarni yangilash
        if not created:
            user.name = name
            user.phone_number = phone_number
            user.role = role
            user.is_staff = is_staff
            user.save()

        # JWT token
        token = AccessToken.for_user(user)

        return Response({
            "access": str(token),
            "user": {
                "id": user.id,
                "telegram_id": user.telegram_id,
                "name": user.name,
                "phone_number": user.phone_number,
                "role": user.role,
                "is_staff": user.is_staff
            }
        }, status=status.HTTP_200_OK)

class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all().order_by("-created_at")
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)