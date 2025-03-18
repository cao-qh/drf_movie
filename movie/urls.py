from django.urls import path, include
from movie import views

app_name = 'movie'
urlpatterns = [
    path('', views.movie_list,name='list'),
    path('<int:pk>/',views.MovieDetail.as_view(),name='detail'),
]
