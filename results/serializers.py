from rest_framework import serializers
from .models import Result


class ResultSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    test = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Result
        fields = [
            'id',
            'user',
            'test',
            'score',
            'created_at'
        ]
