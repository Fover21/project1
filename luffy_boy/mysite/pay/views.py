from rest_framework.views import APIView
from rest_framework.response import Response
from utils.authentication import MyAuth  # 认证类
from utils import redis_poll  # 实现写好的一个redis连接池
from utils.exceptions import CommonException
import redis
from utils.base_response import BaseResponse  # 配置的错误信息类
from course import models
import json  # 存入redis缓存的时候二层以后的字典为字符串，通过json来处理
import datetime
from django.core.exceptions import ObjectDoesNotExist
from utils.pay import AliPay

# Create your views here.
# 往redis中存的数据键值，也就是购物车中有哪些内容的键
# 构建方式为，以用户的id和课程id的拼接 -> 这是为什么呢？ 是为了在查找这个用户买了哪些课程，可以匹配课程(redis可以模糊匹配键)
SHOPPING_CAR_KEY = 'shopping_car_%s_%s'
ACCOUNT_KEY = 'account_%s_%s'
# 接入数据池
REDIS_CONN = redis.Redis(connection_pool=redis_poll.POOL)


# 数据结构
# shopping_car_ %s_ %s: {
#     id: 1,
#     title: CMDB,
#     course_img: xxxxx,
#     price_policy_dict: {
#         1: {有效期1个月， 99}
#
#       }，
#     default_price_policy_id: 3
#
# }
# account_ % s_ % s: {
#     "course_info": {
#         id: 1,
#         title: CMDB,
#         course_img: xxxxx,
#         price_policy_dict: {
#             1: {有效期1个月， 99}
#
# }，
# default_price_policy_id: 3
#
# },
#
# "coupons": {
#     1：{}，
# 3：{}，
# }
# }
#
#
# global_coupon_1: {}


class ShoppingCarView(APIView):
    """
    1030: 加入到购物车失败
    1031：课程不存在
    """
    # 认证，如果要加入购物车，需要先认证，用户是否已经登录！认证通过才可以继续购买，否则需要先登录
    authentication_classes = [MyAuth, ]

    # 加入购入车
    def post(self, request):
        res = BaseResponse()
        try:
            # 1、获取前端传来的course_id 以及price_policy_id
            course_id = request.data.get('course_id', '')
            # print('course_id', course_id)
            price_policy_id = request.data.get('price_policy_id', '')
            # print('price_policy_id', price_policy_id)
            user_id = request.user.id
            # 2、校验数据   验证数据的合法性
            # 2.1、验证course_id是否合法
            course_obj = models.Course.objects.filter(id=course_id).first()
            # print('course_objc', course_obj)
            if not course_obj:
                res.code = 1031
                res.error = '课程不存在'
                return Response(res.dict)
            # 2.2、验证价格策略是否合法
            # 该课程的所有价格策略对象
            price_policy_queryset = course_obj.price_policy.all()
            # 循环获得每个价格策略的详细信息
            price_policy_dict = {}
            for price_policy_obj in price_policy_queryset:
                price_policy_dict[price_policy_obj.id] = {
                    'valid_period_text': price_policy_obj.get_valid_period_display(),
                    'price': price_policy_obj.price
                }
            # 判断价格是否在我们的价格策略里面
            # print('price_policy_dict', price_policy_dict)
            if price_policy_id not in price_policy_dict:
                res.code = 1032
                res.error = '价格策略不存在'
                return Response(res.dict)
            # 3、构建数据结构
            course_info = {
                'id': course_id,
                'title': course_obj.title,
                'course_img': course_obj.course_img,
                'price_policy_dict': json.dumps(price_policy_dict, ensure_ascii=False),
                'default_policy_id': price_policy_id,
            }
            print(course_info)
            # 4、写入redis
            # 4.1、拼接购物车的key
            shopping_car_key = SHOPPING_CAR_KEY % (user_id, course_id)
            print(shopping_car_key)
            # 4.2、写入redis
            REDIS_CONN.hmset(shopping_car_key, course_info)
            res.data = '加入购物车成功'
        except Exception as e:
            print(e)
            res.code = 1031
            res.error = '加入购物车失败'
        return Response(res.dict)

    # 查看购物车
    def get(self, request):
        res = BaseResponse()
        try:
            # 1获取user_id
            user_id = request.user.id
            # print(user_id)
            # 2拼接用户的购物车的key    key支持模糊匹配
            shopping_car_key = SHOPPING_CAR_KEY % (user_id, '*')
            # 3去redis读取该用户的所有加入购物车的内容
            # 3.1先去模糊匹配出所有匹配的key
            all_keys = REDIS_CONN.scan_iter(shopping_car_key)
            # print([i for i in all_keys])  # 迭代器的惰性机制，只能从头读到尾，而且只能读一次
            # 3.2循环所有的keys 得到每个key
            shopping_car_list = []
            for key in all_keys:
                course_info = REDIS_CONN.hgetall(key)
                course_info['price_policy_dict'] = json.loads(course_info['price_policy_dict'])
                shopping_car_list.append(course_info)
            # 返回
            res.data = shopping_car_list
        except Exception as e:
            print(e)
            res.code = 1033
            res.error = '获取购物车失败'
        return Response(res.dict)

    # 更新一条数据
    def put(self, request):
        res = BaseResponse()
        try:
            # 1 获取前端传来的course_id以及price_policy_id
            course_id = request.data.get('course_id', '')
            price_policy_id = request.data.get('price_policy_id', '')
            user_id = request.user.id
            # 2 校验数据的合法性
            # 2.1 校验course_id的合法性
            shopping_car_key = SHOPPING_CAR_KEY % (user_id, course_id)
            if not REDIS_CONN.exists(shopping_car_key):
                res.code = 1035
                res.error = '课程不存在'
                return Response(res.dict)
            # 2.2 判断价格是否合法
            course_info = REDIS_CONN.hgetall(shopping_car_key)
            price_policy_dict = json.loads(course_info['price_policy_dict'])
            if str(price_policy_id) not in price_policy_dict:
                res.code = 1036
                res.error = '所选价格不存在'
                return Response(res.dict)
            # 3 修改redis中的default_policy_id
            course_info['price_policy_id'] = price_policy_id
            # 4 修改信息后写入redis
            REDIS_CONN.hmset(shopping_car_key, course_info)
            res.data = '修改成功'
        except Exception as e:
            print(e)
            res.code = '1034'
            res.error = '更新价格策略失败'
        return Response(res.dict)

    # 删除
    def delete(self, request):
        res = BaseResponse()
        try:
            # 获取前端传过来的course_id
            course_id = request.data.get('course_id', '')
            user_id = request.user.id
            # 2 校验数据的合法性
            # 2.1 校验course_id的合法性
            shopping_car_key = SHOPPING_CAR_KEY % (user_id, course_id)
            if not REDIS_CONN.exists(shopping_car_key):
                res.code = 1039
                res.error = '删除的课程不存在'
                return Response(res.dict)
            # 删除redis中的数据
            REDIS_CONN.delete(shopping_car_key)
            res.data = '删除成功'
        except Exception as e:
            print(e)
            res.code = 1037
            res.error = '删除失败'
        return Response(res.dict)


class AccountView(APIView):
    """
    加入购物车结算接口
    """
    authentication_classes = [MyAuth, ]

    def post(self, request, *args, **kwargs):
        res = BaseResponse()
        # 1 获取数据
        user = request.user
        course_id_list = request.data.get('course_id_list')
        try:
            # 清空操作
            # 找到所有的account_user_id_*,全部清空
            # del_list = REDIS_CONN.keys(ACCOUNT_KEY % (user.pk, "*"))
            # REDIS_CONN.delete(*del_list)
            # 2 循环课程列表为每个课程建立数据结构
            for course_id in course_id_list:
                account_key = ACCOUNT_KEY % (user.pk, course_id)
                account_dict = {}
                shopping_car_key = SHOPPING_CAR_KEY % (user.pk, course_id)
                # 判断课程是否存在购物车中
                if not REDIS_CONN.exists(shopping_car_key):
                    raise CommonException('购物车中该课程不存在', 1040)
                # 将课程信息加入到结算字典中
                course_info = REDIS_CONN.hgetall(shopping_car_key)
                account_dict['course_info'] = course_info

                # 将课程优惠卷加入到每一个课程结算字典中
                # 查询与当前用户拥有没使用的，在有效期且与课程相关的优惠卷
                account_dict['course_coupons'] = self.get_coupon_dict(request, course_id)

                # 存储结算信息
                REDIS_CONN.set(account_key, json.dumps(account_dict))
                # 存储通用优惠卷，加入到redis中
                REDIS_CONN.set('global_coupon_%s' % user.pk, json.dumps(self.get_coupon_dict(request)))
                res.code = 1044
                res.data = '成功'
                # print(json.loads(REDIS_CONN.get(account_key)))
        except CommonException as e:
            res.code = e.code
            res.error = e.msg
        except Exception as e:
            res.code = 500
            res.error = str(e)
        return Response(res.dict)

    def get_coupon_dict(self, request, course_id=None):
        now = datetime.datetime.utcnow()

        coupon_record_list = models.CouponRecord.objects.filter(
            user=request.user,
            status=0,  # 此优惠卷是否被使用
            coupon__valid_begin_date__lte=now,  # 有效期开始时间
            coupon__valid_end_date__gt=now,  # 有效期结束时间
            coupon__object_id=course_id,
            coupon__content_type=10,
        )

        coupon_dict = {}
        for coupon_record in coupon_record_list:
            coupon_dict[coupon_record.pk] = {
                "name": coupon_record.coupon.name,
                "coupon_type": coupon_record.coupon.get_coupon_type_display(),
                "money_equivalent_value": coupon_record.coupon.money_equivalent_value,
                "off_percent": coupon_record.coupon.off_percent,
                "minimum_consume": coupon_record.coupon.minimum_consume,
                "valid_begin_date": coupon_record.coupon.valid_begin_date.strftime("%Y-%m-%d"),
                "valid_end_date": coupon_record.coupon.valid_end_date.strftime("%Y-%m-%d"),
            }
        # print('coupon_dict', coupon_dict)
        return coupon_dict

    def get(self, request, *args, **kwargs):
        res = BaseResponse()
        try:
            # 1获取user_id
            user_id = request.user.id
            print('user', user_id)
            # 2拼接用户要结算的购物车的key    key支持模糊匹配
            account_key = ACCOUNT_KEY % (user_id, '*')
            # 3去redis读取该用户的所有加入购物车的内容
            # 3.1先去模糊匹配出所有匹配的key
            all_keys = REDIS_CONN.keys(account_key)
            # 3.2循环所有的keys 得到每个key
            account_list = {}
            for key in all_keys:
                course_info = REDIS_CONN.get(key)
                account_list['course_info'] = json.loads(course_info)
                account_list['course_info']['course_info']['price_policy_dict'] = json.loads(
                    account_list['course_info']['course_info']['price_policy_dict'])
            account_list['global_coupon_%s' % user_id] = json.loads(REDIS_CONN.get('global_coupon_%s' % user_id))
            # 返回
            res.data = account_list
        except Exception as e:
            print(e)
            res.code = 1033
            res.error = '获取购物车失败'
        return Response(res.dict)


class PaymentView(APIView):
    """
    支付接口
    """
    authentication_classes = [MyAuth, ]

    def post(self, request):
        '''
        {

        "courses_info":[
                     {
                      course_id:1,
                      price_policy_id:1,
                      coupon_record_id:2
                     },
                      {
                      course_id:2,
                      price_policy_id:5,
                      coupon_record_id:3
                     }
                     ]

        global_coupon_id:1,
        beli:1000，
        "pay_money":268,

        }

        :param request:
        :return:
        '''
        # 1 获取数据
        user = request.user
        courses_info = request.data.get('courses_info')
        global_coupon_id = request.data.get('global_coupon_id')
        beili = request.data.get('beili')
        pay_money = request.data.get('pay_money')
        res = BaseResponse()
        now = datetime.datetime.utcnow()
        # 2 循环课程信息
        try:
            course_price_list = []
            for course_info in courses_info:
                course_id = course_info.get('course_id')
                price_policy_id = course_info.get('price_policy_id')
                coupon_record_id = course_info.get('coupon_record_id')
                # 3 校验数据
                # 3.1 课程是否存在
                course_obj = models.Course.objects.get(pk=course_id)

                # 3.2 价格策略是否合法
                if price_policy_id not in [obj.pk for obj in course_obj.price_policy.all()]:
                    raise CommonException('价格策略不存在', 1050)
                # 3.3 课程优惠卷是否合法
                coupon_record = models.CouponRecord.objects.filter(
                    pk=coupon_record_id,
                    user=request.user,
                    status=0,  # 此优惠卷是否被使用
                    coupon__valid_begin_date__lte=now,  # 有效期开始时间
                    coupon__valid_end_date__gt=now,  # 有效期结束时间
                    coupon__object_id=course_id,
                    coupon__content_type=10,
                ).first()

                if not coupon_record:
                    raise CommonException('课程优惠卷不合法', 1052)
                # 3.4 计算课程优惠卷的惠后价格
                course_price = models.PricePolicy.objects.get(pk=price_policy_id).price
                coupon_price = self.cal_coupon_price(course_price, coupon_record)
                course_price_list.append(coupon_price)
            # 4 通用优惠卷处理
            # 4.1 校验通用优惠卷是否合法
            global_coupon_record = models.CouponRecord.objects.filter(
                pk=global_coupon_id,
                user=request.user,
                status=0,  # 此优惠卷是否被使用
                coupon__valid_begin_date__lte=now,  # 有效期开始时间
                coupon__valid_end_date__gt=now,  # 有效期结束时间
                coupon__object_id=None,
                coupon__content_type=10,
            ).first()
            if not global_coupon_record:
                raise CommonException('通用优惠卷不合法', 1053)
            # 4.2 计算通用优惠卷优惠后的价格
            global_coupon_price = self.cal_coupon_price(sum(course_price_list), global_coupon_record)
            # 5 处理贝利
            # 5.1 校验贝利是否充足
            if beili > request.user.beili:
                raise CommonException('贝利不足', 1054)
            # 5.2 计算贝利后的价格
            final_price = global_coupon_price - beili / 10
            print(final_price)
            if final_price < 0:
                final_price = 0
            # 6 比较前端传来的结果(pay_money)和我算出的价格是否一致
            if final_price != pay_money:
                raise CommonException('实际支付价格与参数价格不一致', 1055)
            # 7 订单信息
            # Order记录
            # OrderDetail
            # OrderDetail
            # OrderDetail

            # 8 构建支付宝二维码页面
            import time
            alipay = self.get_alipay()
            # 生成支付的url
            query_params = alipay.direct_pay(
                subject="Django课程",  # 商品简单描述
                out_trade_no="x2" + str(time.time()),  # 商户订单号
                total_amount=pay_money,  # 交易金额(单位: 元 保留俩位小数)
            )

            pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)
            res.data = '订单创建成功'
            res.url = pay_url

        except ObjectDoesNotExist as e:
            print(e)
            res.code = 1050
            res.error = '课程不存在'

        except CommonException as e:
            res.code = e.code
            res.error = e.msg

        except Exception as e:
            res.code = 500
            res.error = str(e)
        return Response(res.dict)

    def cal_coupon_price(self, price, coupon_record):

        coupon_type = coupon_record.coupon.coupon_type
        money_equivalent_value = coupon_record.coupon.money_equivalent_value
        off_percent = coupon_record.coupon.off_percent
        minimum_consume = coupon_record.coupon.minimum_consume
        rebate_price = 0
        if coupon_type == 0:  # 立减卷
            rebate_price = price - money_equivalent_value
            if rebate_price < 0:
                rebate_price = 0
        elif coupon_type == 1:  # 满减卷
            if price < minimum_consume:  # 不满足最低消费
                raise CommonException('不满足最低消费', 1060)
            rebate_price = price - money_equivalent_value
        else:  # 折扣
            rebate_price = price * off_percent / 100
            print(rebate_price)
        return rebate_price

    def get_alipay(self):
        # 沙箱环境地址：https://openhome.alipay.com/platform/appDaily.htm?tab=info
        app_id = "2016091100486897"
        # POST请求，用于最后的检测
        notify_url = "http://47.94.172.250:8804/page2/"
        # notify_url = "http://www.wupeiqi.com:8804/page2/"
        # GET请求，用于页面的跳转展示
        return_url = "http://47.94.172.250:8804/page2/"
        # return_url = "http://www.wupeiqi.com:8804/page2/"
        merchant_private_key_path = "utils/keys/app_private_2048.txt"
        alipay_public_key_path = "utils/keys/alipay_public_2048.txt"

        alipay = AliPay(
            appid=app_id,
            app_notify_url=notify_url,
            return_url=return_url,
            app_private_key_path=merchant_private_key_path,
            alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
            debug=True,  # 默认False,
        )
        return alipay