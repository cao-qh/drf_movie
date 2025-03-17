from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .models import Movie
from .serializers import MovieListSerializer


# Create your views here.
@api_view(['GET','POST'])
def movie_list(request):
    if request.method == 'GET':
        # 获取数据
        movies = Movie.objects.all()
        serializer = MovieListSerializer(movies , many=True)   
        return Response(serializer.data,status=status.HTTP_200_OK)