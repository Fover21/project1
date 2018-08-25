#__author: busensei
#data: 2018/8/13

import my_TCP

sk = my_TCP.My_socket()

sk.bind(('127.0.0.1', 7084))

sk.listen(4)

while 1:

    conn, addr = sk.accept()
    print(conn, type(conn))

    while 1:

        res_s = sk.my_recv(1024, conn)

        print(res_s)

        if res_s == 'q':
            break

        res_f = input('>>>>>')

        sk.my_send(res_f, conn)

        if res_f == 'q':
            break

    conn.close()

sk.close()