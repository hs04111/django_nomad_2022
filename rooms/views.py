from functools import partial
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError
from rest_framework.status import HTTP_204_NO_CONTENT
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from .models import Amenity, Room


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        amenity = AmenitySerializer(data=request.data)
        if amenity.is_valid():
            saved_amenity = amenity.save()
            return Response(AmenitySerializer(saved_amenity).data)
        else:
            return Response(amenity.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenities.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        return Response(AmenitySerializer(self.get_object(pk)).data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity, data=request.data, partial=True)
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        # session에 로그인된 유저가 있는지부터 확인하고 아래 작업을 시작한다.
        # https://docs.djangoproject.com/en/4.1/ref/request-response/#django.http.HttpRequest.user
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                # 카테고리는 클라이언트에서 아이디만 받아 설정할 것
                # 카테고리의 kind가 room인지 experience인지 확인해야 한다.
                category_id = request.data.get("category")
                if not category_id:
                    raise ParseError("Category is required")
                try:
                    category = Category.objects.get(pk=category_id)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")

                # request.data에서 유저 정보를 가져오면 안된다. 유저가 직접 보내면 안됨
                # request.user에는 로그인된 유저가 있다. 이를 보내면 된다.
                # save()를 할 때 추가적인 validated_data를 보내는 방법은 아래와 같다.
                # https://www.django-rest-framework.org/api-guide/serializers/#passing-additional-attributes-to-save
                room = serializer.save(owner=request.user, category=category)

                # amenity는 ManyToManyfield이므로, room이 만들어진 후 amenities를 하나씩 더하는 방식으로 진행한다
                # 만약 amenity가 기존에 존재하지 않는 id를 담고 있으면?
                # 지금 코드처럼 위에서 생성한 room을 지우고, 처음부터 다시 한다.
                # 또는, 없는 id에서도 pass를 except문에 입력하려, 있는 amenity만 입력하도록 한다.
                amenities = request.data.get("amenities")
                for amenity_id in amenities:
                    try:
                        amenity = Amenity.objects.get(pk=amenity_id)
                        room.amenities.add(amenity)
                    except Amenity.DoesNotExist:
                        room.delete()
                        raise ParseError(f"Amenity with id {amenity_id} not found")
                return Response(RoomDetailSerializer(room).data)
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)
