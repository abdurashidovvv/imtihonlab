from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Result
from .serializers import ResultSerializer
from tests.models import Test


class UserTestResultAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, test_id):
        """
        Bitta user + bitta test resultni olish
        """
        result = get_object_or_404(
            Result,
            user=request.user,
            test_id=test_id
        )
        serializer = ResultSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, test_id):
        """
        Result yaratish yoki yangilash
        """
        test = get_object_or_404(Test, id=test_id)

        score = request.data.get('score')

        if score is None:
            return Response(
                {"error": "score majburiy"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result, created = Result.objects.update_or_create(
            user=request.user,
            test=test,
            defaults={'score': score}
        )

        serializer = ResultSerializer(result)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
