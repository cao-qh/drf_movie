
def response_data(status_code=0,message=None,data={},**kwargs):
    return dict({
        'status_code':status_code,
        'message':message,
        'data':data,
    },**kwargs)


class MovieError():
    MovieNotFound = (10001,'电影信息不存在')

class UserError():
    UserNotFound = (20001,'用户信息不存在')
    CollectMovieFail = (20002,'收藏电影失败')
    CancelMovieFailed = (20003,'取消收藏失败')
    NotCollectMovie = (20004,'未收藏该电影')

class TradeError():
    CardParamsError = (30001,'会员卡参数错误')
    OrderCreateError = (30002,'订单创建失败')
    PayRequestError = (30003,'支付请求失败')
    OrderStatusError = (30004,'订单支付状态错误')

