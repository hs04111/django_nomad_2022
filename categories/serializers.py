from importlib.metadata import requires
from typing_extensions import Required
from venv import create
from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        field = "__all__"


# 위의 모델 시리얼라이저를 사용하면 아래와 같은 코드가 포함된다.

# class CategorySerializer(serializers.Serializer):
#     pk = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=50, required=True)
#     kind = serializers.ChoiceField(
#         choices=Category.CategoryKindChoices.choices,
#     )

#     def create(self, validated_data):
#         created_data = Category.objects.create(**validated_data)
#         return created_data

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get("name", instance.name)
#         instance.kind = validated_data.get("kind", instance.kind)
#         instance.save()
#         return instance
