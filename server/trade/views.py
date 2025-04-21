from datetime import datetime
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone


from .models import Card,Order
from account.models import Profile
from .permissions import IsAdminUserOrReadOnly
from .serializers import CardSerializer
from utils.error import TradeError,response_data
from utils.common import get_random_code
from utils.zhifubao import Alipay



# Create your views here.
class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes=[IsAdminUserOrReadOnly]
    
class AlipayAPIView(APIView):
    def get(self,request):
        card_id = request.GET.get('card_id',None)
        try:
            card = Card.objects.get(pk=card_id)
        except:
            return Response(response_data(*TradeError.CardParamsError))
        order_sn = request.GET.get('order_sn',None)
        if not order_sn:
            out_trade_no = "pay" + datetime.now().strftime("%Y%m%d%H%M%S") + get_random_code(4)
            #创建订单
            try:
                Order.objects.create(
                    user = Profile.objects.get(user=request.user),
                    card = card,
                    order_sn=out_trade_no,
                    order_mount=card.card_price,
                    pay_time=timezone.now()
                )
            except:
                return Response(response_data(*TradeError.OrderCreateError))
        else:
            try:
                order = Order.objects.get(order_sn=order_sn)
                if order.pay_status !='PAYING':
                    return Response(response_data(*TradeError.OrderStatusError))
                out_trade_no = order_sn
            except:
                return Response(response_data(*TradeError.OrderStatusError))
        #请求支付
        try:
            alipay = Alipay()
            url = alipay.trade_page(out_trade_no, str(card.card_price), card.card_name, "支付宝测试","FAST_INSTANT_TRADE_PAY")
            return Response(url)
        except:
            return Response(response_data(*TradeError.PayRequestError))

class AlipayCallbackAPIView(APIView):
    def post(self,request):
        params = request.POST.dict()
        print(params)
        return Response('测试回调函数')