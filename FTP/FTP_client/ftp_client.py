# __author: busensei
# data: 2018/9/2

import optparse
import socket
import configparser
import json
import os
import sys


STATUS_CODE = {
    250: 'invalid cmd format',
    251: 'invalid cmd',
    252: 'invalid auth data',
    253: 'wrong username of password',
    254: 'passed authentication',
    255: 'filename doesn\'t provided',
    256: 'file doesn\'t exist on server',
    257: 'ready to send file',
    258: 'md5 verification',

    800: 'the file exist, but not complete, continue?',
    801: 'the file exist!',
    802: 'ready to receive datas',

    900: 'md5 validate successfully'
}


class ClientHandler():

    def __init__(self):
        self.op = optparse.OptionParser()

        self.op.add_option("-s", "--server", dest="server")
        self.op.add_option("-P", "--port", dest="port")
        self.op.add_option("-u", "--username", dest="username")
        self.op.add_option("-p", "--password", dest="password")

        self.options, self.args = self.op.parse_args()

        self.verify_args(self.options, self.args)
        self.make_connection()

        # 保存当前路径
        self.mainPath = os.path.dirname(os.path.abspath(__file__))
        #进度条
        self.last = 0

    def verify_args(self, options, args):
        server = options.server
        port = options.port
        # username = options.username
        # password = options.password

        # 检验
        if int(port) > 0 and int(port) < 65535:
            return True
        else:
            exit('The port is in 0~65535')

    # 链接
    def make_connection(self):

        self.sock = socket.socket()
        self.sock.connect((self.options.server, int(self.options.port)))

    # 交互
    def interactive(self):
        # 验证成功
        if self.authenticate():
            print('begin to interactive......')
            while 1:
                cmd_info = input("[%s]" % self.current_dir).strip()  # put images
                cmd_list = cmd_info.split()
                if hasattr(self, cmd_list[0]):
                    func = getattr(self, cmd_list[0])
                    func(*cmd_list)

    # 上传
    def put(self, *cmd_list):
        # put传 文件路径 指定上传到哪 filename filesize
        action, local_path, target_path = cmd_list
        # 路径拼接 获得本地绝对路径
        local_path = os.path.join(self.mainPath, local_path)

        file_name = os.path.basename(local_path)
        file_size = os.stat(local_path).st_size

        data = {
            "action": "put",
            "file_name": file_name,
            "file_size": file_size,
            # 传到哪
            "target_path": target_path
        }

        self.sock.send(json.dumps(data).encode('utf-8'))

        is_exits = self.sock.recv(1024).decode('utf-8')
        #####################
        has_sent = 0
        if is_exits == '800':
            # 文件不完整
            choice = input("the file exist, but not enough, is coutinue?[Y/N]").strip()
            if choice.upper() == 'Y':
                self.sock.sendall('Y'.encode('utf-8'))
                continue_position = self.sock.recv(1024).decode('utf-8')
                has_sent += int(continue_position)

            else:
                self.sock.sendall('N'.encode('utf-8'))


        elif is_exits == '801':
            # 文件完全存在
            print('The file is exist!')
            return

        f = open(local_path, 'rb')
        f.seek(has_sent)
        while has_sent < file_size:
            data = f.read(1024)
            self.sock.sendall(data)
            has_sent += len(data)
            self.show_progress(has_sent, file_size)

        f.close()
        print('put success!')

    #进度条
    def show_progress(self, has, total):
        rate = float(has)/float(total)
        rate_num = int(rate * 100)
        if self.last != rate_num:
            sys.stdout.write("%s%% %s\r" % (rate_num, "#"*rate_num))
        self.last = rate_num

    def ls(self, *cmd_list):
        data = {
            "action": "ls"
        }
        self.sock.sendall(json.dumps(data).encode('utf-8'))
        data = self.sock.recv(1024).decode('utf-8')
        print(data)

    def cd(self, *cmd_list):
        #cd 目录
        data = {
            "action": "cd",
            "dirname": cmd_list[1]
        }
        self.sock.sendall(json.dumps(data).encode('utf-8'))
        data = self.sock.recv(1024).decode('utf-8')
        self.current_dir = data
        print(os.path.basename(data))
        self.current_dir = os.path.basename(data)

    def mkdir(self, *cmd_list):
        data = {
            "action": "mkdir",
            "dirname":cmd_list[1]
        }
        self.sock.sendall(json.dumps(data).encode('utf-8'))
        data = self.sock.recv(1024).decode('utf-8')

    # 验证
    def authenticate(self):
        if self.options.username is None or self.options.password is None:
            username = input("username:")
            password = input("password:")
            return self.get_auth_result(username, password)
        else:
            return self.get_auth_result(self.options.username, self.options.password)

    # 收发
    def response(self):
        data = self.sock.recv(1024).decode('utf-8')
        data = json.loads(data)
        return data

    def get_auth_result(self, user, pwd):

        data = {
            "action": "auth",
            "username": user,
            "password": pwd
        }
        self.sock.send(json.dumps(data).encode('utf-8'))

        response = self.response()
        print("response", response["status_code"])

        if response["status_code"] == 254:
            self.user = user
            self.current_dir = user
            print(STATUS_CODE)
            return True
        else:
            print(STATUS_CODE['status_code'])


ch = ClientHandler()

# 交互
ch.interactive()
