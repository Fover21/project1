# __author: ward
# data: 2018/11/22

class BaseResponse(object):

    def __init__(self):
        self.code = 1000
        self.error = ''
        # 成功的数据
        self.data = ''

    # 将信息属性值信息封装为属性
    @property
    def dict(self):
        # 将该类中属性值以字典形式返回
        return self.__dict__
