# __author: busensei
# data: 2018/8/13

import socket


class My_socket(socket.socket):

    def __init__(self, encoding='utf-8'):
        self.encoding = encoding
        super(My_socket, self).__init__()


    def mysend(self, data):
        return super(My_socket, self).send(data.encode(self.encoding))

    def my_send(self, data, conn):
        return conn.send(data.encode(self.encoding))

    def myrecv(self, num):
        msg = super(My_socket, self).recv(num).decode(self.encoding)
        return msg

    def my_recv(self, buffersize, conn):
        msg = conn.recv(buffersize).decode(self.encoding)
        return msg
