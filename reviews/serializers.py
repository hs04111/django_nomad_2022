from rest_framework import serializers
from users.serializers import TinyUserSerializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):

    user = TinyUserSerializers(read_only=True)

    class Meta:
        model = Review
        exclude = (
            "room",
            "experience",
        )
