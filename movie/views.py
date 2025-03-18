from django.shortcuts import render
from django.http import Http404, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins

from .models import Movie
from .serializers import MovieListSerializer,MovieDetailSerializer


# Create your views here.
@api_view(['GET','POST'])
def movie_list(request):
    if request.method == 'GET':
        # 获取数据
        movies = Movie.objects.all()
        serializer = MovieListSerializer(movies , many=True)   
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = MovieListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
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

class MovieDetail(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializer
    
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    
    def put(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)
    
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)