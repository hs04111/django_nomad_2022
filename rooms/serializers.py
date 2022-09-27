from dataclasses import field
from rest_framework.serializers import ModelSerializer
from users.serializers import TinyUserSerializers
from categories.serializers import CategorySerializer
from .models import Amenity, Room


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "name",
            "country",
            "city",
            "price",
            "pk",
        )
        # 아래와 같이 두면 relationship을 가진 모든 데이터를 가져온다.
        # 이러면 과하다. 차라리 용도에 따라 serializer를 나누는 것이 현명하다.
        # depth = 1


class RoomDetailSerializer(ModelSerializer):

    # relation을 가진 데이터를 가져오려면 아래와 같이 serializer를 해당 field에 부여한다.
    # 어떤 field를 가져올지는 해당 serializer에서 조정한다.
    # read_only=True로 두어서, room을 만들 때 post request때 data에 들어있지 않아도 is_valid()=True가 되도록 만들고
    # save()에서 추가적인 data를 보내는 것으로 작업한다.
    owner = TinyUserSerializers(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Room
        fields = "__all__"
