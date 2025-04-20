from django.shortcuts import render
from rest_framework import viewsets
from .models import Card
from .permissions import IsAdminUserOrReadOnly
from .serializers import CardSerializer

# Create your views here.
class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes=[IsAdminUserOrReadOnly]