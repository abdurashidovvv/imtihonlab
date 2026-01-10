from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Test
from .serializers import TestCreateSerializer
from .permissions import IsAdminUserCustom
from .serializers import TestGetSerializer


class TestCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserCustom]

    def post(self, request):
        serializer = TestCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        test = serializer.save(created_by=request.user)

        return Response(
            {
                "message": "Test successfully uploaded",
                "test_id": test.id,
                "title": test.title
            },
            status=status.HTTP_201_CREATED
        )


class TestListView(APIView):
    def get(self, request):
        tests = Test.objects.all().order_by("-created_at")
        serializer = TestGetSerializer(tests, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestDetailView(APIView):
    def get(self, request, id):
        try:
            test = Test.objects.get(id=id)
        except Test.DoesNotExist:
            return Response({"error": "Test not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TestGetSerializer(test, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
