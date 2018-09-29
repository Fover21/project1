# __author: busensei
# data: 2018/9/2

import optparse  # 解析命令行命令
import socketserver
from conf import settings
from core import server


class ArgvHandler():

    def __init__(self):
        self.op = optparse.OptionParser()

        # self.op.add_option("-s", "--server", dest="server")
        # self.op.add_option("-P", "--port", dest="port")

        options, args = self.op.parse_args()

        # print(options)  # 绑定的键值对    #是一个对象不是字典，.server拿值
        # print(args)  # 没有绑定的信息列表

        self.varyfy_args(options, args)

    # 命令的分发，增加功能
    def varyfy_args(self, options, args):
        cmd = args[0]

        if hasattr(self, cmd):
            func = getattr(self, cmd)
            func()

    def start(self):
        print('The server is working')
        s = socketserver.ThreadingTCPServer((settings.IP, settings.PORT), server.ServerHandler)
        s.serve_forever()

    def help(self): pass
