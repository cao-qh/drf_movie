"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from movie import views
from account import views as account_views
from trade import views as trade_views


router = DefaultRouter()
router.register(r"movie", views.MovieViewSet)
router.register(r"category", views.CategoryViewSet)
router.register(r"collects", account_views.CollectViewSet, 'collects')
router.register(r'cards',trade_views.CardViewSet,'cards')
router.register(r'orders',trade_views.OrderViewSet,'orders')


urlpatterns = [
    path("admin/", admin.site.urls),
    # path('api/movie/',include('movie.urls',namespace='movie'))
    path("api/", include(router.urls)),
    path("api/", include("djoser.urls")),
    path("api/", include("djoser.urls.jwt")),
    path('api/alipay/',trade_views.AlipayAPIView.as_view()),
    path('api/callback/',trade_views.AlipayCallbackAPIView.as_view()),
    path('api/tasks/',trade_views.TaskAPIView.as_view()),
]
