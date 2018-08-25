#__author: busensei
#data: 2018/8/13

import socket


class My_Socket(socket.socket):

    def __init__(self, encoding='utf-8'):
        self.encoding = encoding
        super(My_Socket, self).__init__(type=socket.SOCK_DGRAM)

    def mysendto(self, msg, addr):
        return self.sendto(msg.encode(self.encoding), addr)

    def myrecvfrom(self, num):
        data, addr = self.recvfrom(num)
        return data.decode(self.encoding), addr
