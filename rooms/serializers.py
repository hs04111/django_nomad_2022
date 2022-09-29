from dataclasses import field
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from users.serializers import TinyUserSerializers
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist
from .models import Amenity, Room


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomListSerializer(ModelSerializer):

    # ModelSerializer에서는 model에서 method로 정의된 field는 가져오지 않는다.
    # 이를 가져오고 싶으면 아래와 같이 작성하면 가져올 수 있다.
    # serializer의 method 이름은 get_fieldname으로 작성해야 한다.

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        # APIview에서 serializer에 context로 넣은 dict를 아래와 같이 사용 가능하다.
        return self.context.get("request").user == room.owner

    def get_is_liked(self, room):
        request = self.context.get("request")
        return Wishlist.objects.filter(user=request.user, rooms__pk=room.pk).exists()

    class Meta:
        model = Room
        fields = (
            "name",
            "country",
            "city",
            "price",
            "pk",
            "rating",
            "is_owner",
            "is_liked",
            "photos",
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
    photos = PhotoSerializer(many=True, read_only=True)

    # reverse relationship. 아래처럼만 작성해도 room을 가리키는 review들을 가져올 수 있다.
    # reviews = ReviewSerializer(many=True, read_only=True)
    # 그런데 위처럼 하면 pagination이 적용되지 않아, 모든 리뷰를 한번에 가져와버린다.
    # DB가 힘들어하므로, 아예 review를 가져오는 url을 하나 더 설정하는 방향으로 해서
    # pagination을 적용하기로 한다.

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, room):
        # APIview에서 serializer에 context로 넣은 dict를 아래와 같이 사용 가능하다.
        return self.context.get("request").user == room.owner

    def get_rating(self, room):
        return room.rating()

    class Meta:
        model = Room
        fields = "__all__"
