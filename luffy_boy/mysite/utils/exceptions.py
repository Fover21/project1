# __author: ward
# data: 2018/11/26


class CommonException(Exception):
    def __init__(self, msg, code):
        self.msg = msg
        self.code = code
