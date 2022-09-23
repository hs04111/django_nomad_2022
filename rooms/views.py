from functools import partial
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from .serializers import AmenitySerializer, RoomSerializer
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
        serializer = RoomSerializer(all_rooms, many=True)
        return Response(serializer.data)
