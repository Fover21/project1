# __author: busensei
# data: 2018/11/26

import redis
from utils.redis_poll import POOL
r = redis.Redis(connection_pool=POOL)

# print(r.keys('global_coupon_1'))coupon_dict
# print(r.get('global_coupon_1'))
print(r.keys())