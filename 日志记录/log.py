# __author: busensei
# data: 2018/8/13





# 1.创建一个logger对象
# 2.创建一个文件管理操作符
# 3.创建一个屏幕管理操作符
# 4.创建一个日志输出格式
# 5.给文件操作符绑定一个格式
# 6.给屏幕管理操作符绑定一个格式
# 7.logger对象绑定文件管理操作符
# 8.logger对象绑定屏幕管理操作符

import logging
import time
import os

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename='test.log',
#                     filemode='a')



data = time.strftime('%Y-%m-%d', time.localtime())
# time.strftime('%Y-%m-%d'), time.localtime()
# print(data)

# 创建一个logger对象
logger = logging.getLogger()


path = os.path.dirname(os.path.abspath(__file__))

data = data + '.txt'

data = '/'.join([path, data])

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler(data, mode='a', encoding='utf-8')

# 在创建一个handler，用于输出到控制台
sh = logging.StreamHandler()

# 创建一个日志输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 给文件管理操作符绑定一个格式
fh.setFormatter(formatter)

# 给屏幕管理操作符绑定一个格式
sh.setFormatter(formatter)

# logger对象绑定文件管理操作符
logger.addHandler(fh)

# logger对象绑定屏幕管理操作符
logger.addHandler(sh)

# 设置级别
# fh.setLevel(logging.DEBUG)
# sh.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
# logging.debug('debug message')
# logging.info('info message')
# logging.warning('waring message')
# logging.error('error message')
# logging.critical('critical message')
