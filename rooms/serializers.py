from dataclasses import field
from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        # 아래와 같이 두면 relationship을 가진 모든 데이터를 가져온다.
        # 이러면 과하다. 차라리 용도에 따라 serializer를 나누는 것이 현명하다.
        # depth = 1
