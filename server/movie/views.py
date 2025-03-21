from django.shortcuts import render
from django.http import Http404, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets
from django_filters import rest_framework as filters

from .models import Movie,Category
from .serializers import MovieSerializer,CategorySerializer


# Create your views here.
# @api_view(['GET','POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         # 获取数据
#         movies = Movie.objects.all()
#         serializer = MovieListSerializer(movies , many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = MovieListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# class MovieDetail(APIView):
#     def get(self,request,pk):
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except:
#             raise Http404
#         serializer = MovieDetailSerializer(movie)
#         return Response(serializer.data)

#     def put(self,request,pk):
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except:
#             raise Http404

#         serializer = MovieDetailSerializer(movie,data=request.data,partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status =status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#     def delete(self,request,pk):
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except:
#             raise Http404
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class MovieList(generics.ListCreateAPIView):
#     queryset = Movie.objects.all()
#     serializer_class = MovieListSerializer

# class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Movie.objects.all()
#     serializer_class = MovieDetailSerializer

class MovieFilter(filters.FilterSet):
    movie_name = filters.CharFilter(lookup_expr='icontains')
    category_id = filters.NumberFilter()
    region = filters.NumberFilter()
    
    class Meta:
        model = Movie
        fields = ['movie_name']

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('movie_name',)
    filterset_class = MovieFilter
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer