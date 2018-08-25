# __author: busensei
# data: 2018/8/13

import socket
import sys
import os
import json
import struct

sk = socket.socket()
adress = ('192.168.12.11', 29231)


def upload():
    message = {'filename': None, 'filesize': None}
    sk.connect(adress)
    temp = '上传'
    sk.send(temp.encode('utf-8'))
    meg = input('输入文件路径：')
    filename = os.path.basename(meg)
    filesize = os.path.getsize(meg)
    message['filename'] = filename
    message['filesize'] = filesize
    str_message = json.dumps(message)
    len_message = len(str_message)
    b_len_message = struct.pack('i', len_message)
    sk.send(b_len_message + str_message.encode('utf-8'))
    with open(meg, 'rb') as f:
        while filesize:
            connent = f.read()
            sk.send(connent)
            filesize -= len(connent)


def download():
    path = os.path.dirname(os.path.abspath(__file__))
    sk.connect(adress)
    temp = '下载'
    sk.send(temp.encode('utf-8'))
    num = sk.recv(1024).decode('utf-8')
    print('可下载文件：%s' % (num,))
    name = input('输入下载文件名称：')
    sk.send(name.encode('utf-8'))
    path = '/'.join([path, '本地文件', name])
    b_len_message = sk.recv(4)
    len_message = struct.unpack('i', b_len_message)[0]
    res_s = sk.recv(len_message).decode('utf-8')
    str_message = json.loads(res_s)
    filesize = str_message['filesize']
    with open(path, 'ab') as f:
        while filesize:
            connent = sk.recv(1024)
            f.write(connent)
            f.flush()
            filesize -= len(connent)


def main():
    dic = [
        ('上传', 'upload'),
        ('下载', 'download')
    ]
    for i in enumerate(dic, 1):
        print(i[0], i[1][0])
    num = int(input('请输入选项:'))
    getattr(sys.modules[__name__], dic[num - 1][1])()
    sk.close()


if __name__ == '__main__':
    main()
