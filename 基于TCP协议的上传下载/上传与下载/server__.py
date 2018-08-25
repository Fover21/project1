# __author: busensei
# data: 2018/8/13


import socket
import struct
import os
import json

path = os.path.abspath(__file__)
path = os.path.dirname(path)
sk = socket.socket()
adress = ('0.0.0.0', 29231)
sk.bind(adress)
sk.listen(4)
conn, addr = sk.accept()


def upload(path):
    b_len_message = conn.recv(4)
    len_message = struct.unpack('i', b_len_message)[0]
    res_s = conn.recv(len_message).decode('utf-8')
    str_message = json.loads(res_s)
    filename = '1' + str_message['filename']
    filesize = str_message['filesize']
    path = '/'.join([path, '客户端上传的文件', filename])
    with open(path, 'ab') as f:
        while filesize:
            connent = conn.recv(1024)
            f.write(connent)
            f.flush()
            filesize -= len(connent)


def download(path):
    message = {'filename': None, 'filesize': None}
    res = os.listdir('/'.join([path, '客户端上传的文件']))
    sum = ''
    for i in res:
        sum = sum + ' ' + i + '    '
    conn.send(sum.encode('utf-8'))
    filename = conn.recv(1024).decode('utf-8')
    path = '/'.join([path, '客户端上传的文件', filename])
    filesize = os.path.getsize(path)
    message['filename'] = path
    message['filesize'] = filesize
    str_message = json.dumps(message)
    len_message = len(str_message)
    b_len_message = struct.pack('i', len_message)
    conn.send(b_len_message + str_message.encode('utf-8'))

    with open(path, 'rb') as f:
        while filesize:
            connent = f.read()
            conn.send(connent)
            filesize -= len(connent)


def main():
    res_s = conn.recv(1024).decode('utf-8')
    if res_s == '上传':
        upload(path)
        sk.close()
    if res_s == '下载':
        download(path)
        sk.close()


if __name__ == '__main__':
    while 1:
        main()
