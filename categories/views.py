from functools import partial
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import CategorySerializer
from .models import Category

# Create your views here.


# 아래에 작성한 코드는 아래의 3줄로 모두 대체 가능하다:
# class CategoryViewset(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

# urls.py에서는 as_view()에 인자로 각 http method마다 어떤 method를 사용할지 표시해야 한다
# viewset에 포함된 method들은 아래 링크 참조
# https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions
# 아래는 예시
# urlpatterns = [
#     path("", views.CategoryViewset.as_view({
#         'get':'list',
#         'post':'create'
#     })),
#     path("<int:pk>/", views.CategoryViewset.as_view({
#         'get':'retrieve',
#         'put':'partial_update',
#         'delete':'destroy'
#     })),
# ]


class Categories(APIView):
    def get(self, request):
        serialized_categories = CategorySerializer(
            Category.objects.all(),
            many=True,
        )
        return Response(serialized_categories.data)

    def post(self, request):
        category_data = CategorySerializer(data=request.data)
        if category_data.is_valid():
            saved_data = category_data.save()
            serialized_categories = CategorySerializer(saved_data).data
            return Response(serialized_categories)
        else:
            return Response(category_data.errors)


# @api_view(["GET", "POST"])
# def categories(request):
#     if request.method == "GET":
#         serialized_categories = CategorySerializer(
#             Category.objects.all(),
#             many=True,
#         )
#         return Response(serialized_categories.data)
#     elif request.method == "POST":
#         category_data = CategorySerializer(data=request.data)
#         if category_data.is_valid():
#             saved_data = category_data.save()
#             serialized_categories = CategorySerializer(saved_data).data
#             return Response(serialized_categories)
#         else:
#             return Response(category_data.errors)


class CategoryDetail(APIView):
    def get_object(self, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound
        return category

    def get(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = CategorySerializer(
            self.get_object(pk),
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)


# @api_view(["GET", "PUT", "DELETE"])
# def category(request, pk):
#     try:
#         category = Category.objects.get(pk=pk)
#     except Category.DoesNotExist:
#         return Response(NotFound)
#     if request.method == "GET":
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)
#     elif request.method == "PUT":
#         serializer = CategorySerializer(category, data=request.data, partial=True)
#         if serializer.is_valid():
#             updated_category = serializer.save()
#             return Response(CategorySerializer(updated_category).data)
#         else:
#             return Response(serializer.errors)
#     elif request.method == "DELETE":
#         category.delete()
#         return Response(status=HTTP_204_NO_CONTENT)
