#__author: busensei
#data: 2018/8/13

import my_UDP


sk = my_UDP.My_Socket()

sk.bind(('127.0.0.1', 8080))

while 1:

    data, addr = sk.myrecvfrom(1024)

    print(data)

    msg = input('>>>')

    sk.mysendto(msg, addr)