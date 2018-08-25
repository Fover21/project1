#__author: busensei
#data: 2018/8/14

import socket


sk = socket.socket()
sk.connect_ex(('127.0.0.1', 8888))
msg1 = sk.recv(1024)
print('msg1:', msg1)
msg2 = sk.recv(1024)
print('msg2:', msg2)
sk.close()
