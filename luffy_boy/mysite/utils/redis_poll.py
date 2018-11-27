# __author: busensei
# data: 2018/11/23

import redis

# POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
POOL = redis.ConnectionPool(host='192.168.12.73', port=6379, decode_responses=True)
