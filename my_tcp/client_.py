#__author: busensei
#data: 2018/8/13

import my_TCP

sk = my_TCP.My_socket()

adress = ('127.0.0.1', 7084)

sk.connect(adress)

while 1:

    meg = input('>>>')

    sk.mysend(meg)

    if meg == 'q':
        break

    res_s = sk.myrecv(1024)

    if res_s == 'q':
        break

    print(res_s)

sk.close()