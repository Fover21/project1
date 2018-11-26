from rest_framework.views import APIView
from rest_framework.response import Response
from utils.authentication import MyAuth  # 认证类
from utils import redis_poll  # 实现写好的一个redis连接池
import redis
from utils.base_response import BaseResponse  # 配置的错误信息类
from course import models
import json  # 存入redis缓存的时候二层以后的字典为字符串，通过json来处理

# Create your views here.
# 往redis中存的数据键值，也就是购物车中有哪些内容的键
# 构建方式为，以用户的id和课程id的拼接 -> 这是为什么呢？ 是为了在查找这个用户买了哪些课程，可以匹配课程(redis可以模糊匹配键)
SHOPPING_CAR_KEY = 'shopping_car_%s_%s'
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
