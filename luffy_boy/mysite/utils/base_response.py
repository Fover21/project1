# __author: ward
# data: 2018/11/22

class BaseResponse(object):

    def __init__(self):
        self.code = 1000
        self.error = ''
        # 成功的数据
        self.data = ''

    @property
    def dict(self):
        return self.__dict__
