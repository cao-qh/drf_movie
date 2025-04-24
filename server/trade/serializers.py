from rest_framework import serializers
from .models import Card,Order

class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ['id','card_name','card_price','info','duration']
        
class OrderSerializer(serializers.ModelSerializer):
    card = CardSerializer()
    class Meta:
        model = Order
        fields = ['id','order_sn','pay_status','order_mount','created_at','card']