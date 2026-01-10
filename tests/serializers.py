from rest_framework import serializers
from .models import Test


class TestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = [
            "title",
            "description",
            "test_file",
            "answer_file",
            "open_questions_count",
            "closed_questions_count",
        ]

class TestGetSerializer(serializers.ModelSerializer):
    test_file_url = serializers.SerializerMethodField()
    answer_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = [
            "id",
            "title",
            "description",
            "open_questions_count",
            "closed_questions_count",
            "created_by",
            "created_at",
            "test_file_url",
            "answer_file_url"
        ]

    def get_test_file_url(self, obj):
        request = self.context.get("request")
        if obj.test_file and hasattr(obj.test_file, 'url'):
            return request.build_absolute_uri(obj.test_file.url) if request else obj.test_file.url
        return None

    def get_answer_file_url(self, obj):
        request = self.context.get("request")
        if obj.answer_file and hasattr(obj.answer_file, 'url'):
            return request.build_absolute_uri(obj.answer_file.url) if request else obj.answer_file.url
        return None

