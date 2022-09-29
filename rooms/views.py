from functools import partial
from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_204_NO_CONTENT
from categories.models import Category
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from .models import Amenity, Room
from rooms import serializers


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

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        # 아래처럼 serializer에 context를 dict로 넣으면
        # serializer의 method 들에서 self.context로 사용할 수 있다.

        serializer = RoomListSerializer(
            all_rooms, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        # session에 로그인된 유저가 있는지부터 확인하고 아래 작업을 시작한다.
        # https://docs.djangoproject.com/en/4.1/ref/request-response/#django.http.HttpRequest.user
        # 이전 코드에서는 user.is_authenticated로 보았지만, 이제 permission class로 대체한다.
        # isAuthenticatedOrReadOnly는 get에서는 모두 허용, post는 인증되어야 한다.
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

            # amenity는 ManyToManyfield이므로, room이 만들어진 후 amenities를 하나씩 더하는 방식으로 진행한다
            # 만약 amenity가 기존에 존재하지 않는 id를 담고 있으면?
            # 지금 코드처럼 위에서 생성한 room을 지우고, 처음부터 다시 한다.
            # 또는, 없는 id에서도 pass를 except문에 입력하려, 있는 amenity만 입력하도록 한다.

            # transaction: Django는 기본적으로 autocommit 모드이다. 즉, 각각의 query가 transaction으로 둘러싸여
            # 하나씩 commit되거나, 하나씩 roll back된다.
            # 만약 여러 query를 django가 내부적으로 검토하고 한번에 commit되도록 하고 싶다면
            # transaction.atomic을 사용하여 아래와 같이 코드를 작성한다.
            try:
                with transaction.atomic():
                    room = serializer.save(owner=request.user, category=category)
                    amenities = request.data.get("amenities")
                    for amenity_id in amenities:
                        amenity = Amenity.objects.get(pk=amenity_id)
                        room.amenities.add(amenity)
                    return Response(RoomDetailSerializer(room).data)
            except Exception:
                raise ParseError("Amenity not found")
        else:
            return Response(serializer.errors)


class RoomDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied
        serializer = RoomDetailSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            category_id = request.data.get("category")
            if category_id:
                try:
                    category = Category.objects.get(pk=category_id)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")

            try:
                with transaction.atomic():
                    if category_id:
                        room = serializer.save(category=category)
                    else:
                        room = serializer.save()
                    amenities = request.data.get("amenities")
                    if amenities:
                        room.amenities.clear()
                        for amenity_id in amenities:
                            amenity = Amenity.objects.get(pk=amenity_id)
                            room.amenities.add(amenity)
                    return Response(RoomDetailSerializer(room).data)
            except Exception:
                raise ParseError("Amenity not found")
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = self.get_object(pk)

        if request.user != room.owner:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        page = request.query_params.get("page", 1)
        try:
            page = int(page)
        except ValueError:
            page = 1

        serializer = ReviewSerializer(
            room.reviews.all()[3 * (page - 1) : 3 * page], many=True
        )
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(user=request.user, room=room)
            return Response(ReviewSerializer(review).data)
        else:
            return Response(serializer.errors)


class RoomAmenitiesList(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        page = request.query_params.get("page", 1)
        try:
            page = int(page)
        except ValueError:
            page = 1

        serializer = AmenitySerializer(
            room.amenities.all()[3 * (page - 1) : 3 * page], many=True
        )
        return Response(serializer.data)


class RoomPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            return Response(PhotoSerializer(photo).data)
        else:
            return Response(serializer.errors)
