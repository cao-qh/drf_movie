from datetime import datetime
from datetime import timedelta
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,IsAuthenticated,SAFE_METHODS
from django.utils import timezone
from django.db import transaction
from django.conf import settings


from .models import Card, Order
from account.models import Profile
from .permissions import IsAdminUserOrReadOnly
from .serializers import CardSerializer,OrderSerializer
from utils.error import TradeError, response_data
from utils.common import get_random_code
from utils.zhifubao import Alipay
from utils.filters import OrderFilter


# Create your views here.
class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class AlipayAPIView(APIView):
    def get(self, request):
        card_id = request.GET.get("card_id", None)
        try:
            card = Card.objects.get(pk=card_id)
        except:
            return Response(response_data(*TradeError.CardParamsError))
        order_sn = request.GET.get("order_sn", None)
        if not order_sn:
            out_trade_no = (
                "pay" + datetime.now().strftime("%Y%m%d%H%M%S") + get_random_code(4)
            )
            # 创建订单
            try:
                Order.objects.create(
                    user=Profile.objects.get(user=request.user),
                    card=card,
                    order_sn=out_trade_no,
                    order_mount=card.card_price,
                    pay_time=timezone.now(),
                )
            except:
                return Response(response_data(*TradeError.OrderCreateError))
        else:
            try:
                order = Order.objects.get(order_sn=order_sn)
                if order.pay_status != "PAYING":
                    return Response(response_data(*TradeError.OrderStatusError))
                out_trade_no = order_sn
            except:
                return Response(response_data(*TradeError.OrderStatusError))
        # 请求支付
        try:
            alipay = Alipay()
            url = alipay.trade_page(
                out_trade_no,
                str(card.card_price),
                card.card_name,
                "支付宝测试",
                "FAST_INSTANT_TRADE_PAY",
            )
            return Response(url)
        except:
            return Response(response_data(*TradeError.PayRequestError))


class AlipayCallbackAPIView(APIView):
    def post(self, request):
        params = request.POST.dict()
        print(params)
        # 去除sign sign_type
        sign = params.pop("sign")
        del params["sign_type"]
        # 对字典进行排序
        sorted_list = sorted([(k, v) for k, v in params.items()])
        unsigned_string = "&".join(
            f"{k}={v}" for k, v in sorted_list
        )  # out_trade_nopay=202502161810110168&product_code=FAST_INSTANT_TRADE_PAY
        alipay = Alipay()
        if not alipay.verify_sign(unsigned_string, sign):
            print("verify_sign_error")
            return Response("error")
        # 验证out_trade_no
        try:
            order = Order.objects.get(order_sn=params.get("out_trade_no"))
        except:
            return Response("error")
        if params.get("total_amount") != str(order.order_mount):
            return Response("error")
        if params.get("seller_id") != settings.ALIPAY_SELLER_ID:
            return Response("error")
        if params.get("app_id") != settings.ALIPAY_APP_ID:
            return Response("error")
        if params.get("trade_status") not in ["TRADE_SUCCESS", "TRADE_FINISHED"]:
            return Response("error")
        # 业务逻辑
        print("全部验证通过")
        # 更改order表,使用事务
        with transaction.atomic():
            order.trade_no = params.get("trade_no")
            order.pay_status = params.get("trade_status")
            order.pay_time = datetime.now()
            order.save()
            # 更改profile表
            profile = Profile.objects.get(uid=order.user.uid)
            profile.is_upgrade = 1
            profile.upgrade_time = datetime.now()
            profile.upgrade_count += 1
            # 如果用户首次充值，或者会员已经过期，设置过期时长为当前时间+会员卡时长
            # 如果会员未过期，过期时长为原过期时长+会员卡时长
            if not profile.expire_time or profile.expire_time < timezone.now():
                profile.expire_time = datetime.now() + timedelta(
                    days=order.card.duration
                )
            else:
                profile.expire_time = profile.expire_time + timedelta(
                    days=order.card.duration
                )
            profile.save()

        return Response("success")

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.order_by('-id')
    serializer_class = OrderSerializer
    filterset_class = OrderFilter

    def get_queryset(self):
        profile = self.request.user.profile
        return Order.objects.filter(user=profile).order_by('-id')

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        else:
            return [IsAdminUser]