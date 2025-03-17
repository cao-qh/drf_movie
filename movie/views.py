from django.shortcuts import render
from django.http import JsonResponse

from .models import Movie


# Create your views here.
def movie_list(request):
    # 获取数据
    # movies = Movie.objects.all().values_list()
    # data = list(movies)
    data = {
        'movie_name':'碟中谍',
        'rate':7.8
    }
    return JsonResponse(data , safe=False)