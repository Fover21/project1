# __author: busensei
# data: 2018/9/2

import socketserver
import json
import configparser
from conf import settings
import os

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


class ServerHandler(socketserver.BaseRequestHandler):

    def handle(self):

        while 1:
            data = self.request.recv(1024).strip()
            data = json.loads(data.decode('utf-8'))
            '''
                {
                    "action":"auth",/"put"/
                    "username":" ",
                    "password":" "
                }
            '''
            if data.get('action'):
                if hasattr(self, data.get("action")):
                    func = getattr(self, data.get("action"))
                    func(**data)

                else:
                    print('Incalid cmd')
            else:
                print("Incalid cmd")

    def send_reponss(self, state_code):
        response = {"status_code": state_code}

        self.request.sendall(json.dumps(response).encode('utf-8'))

    def auth(self, **data):

        username = data['username']
        password = data['password']

        user = self.authenticate(username, password)
        if user:
            self.send_reponss(254)
        else:
            self.send_reponss(253)

    def authenticate(self, user, pwd):
        cfg = configparser.ConfigParser()
        cfg.read(settings.ACCOUNT_PATH)

        if user in cfg.sections():
            if cfg[user]["Password"] == pwd:
                self.user = user
                self.mainPath = os.path.join(settings.BASE_DIR, "home", self.user)
                print('passed authentication')
                return user

    # 上传
    def put(self, **data):
        print("data", data)
        file_name = data.get("file_name")
        file_size = data.get("file_size")
        target_path = data.get("target_path")
        print(file_name, file_size, target_path)

        abs_path = os.path.join(self.mainPath, target_path, file_name)
        print(abs_path)
        ##############################
        has_received = 0
        if os.path.exists(abs_path):
            file_has_size = os.stat(abs_path).st_size
            if file_has_size < file_size:
                # 断点续传
                self.request.sendall('800'.encode('utf-8'))
                choice = self.request.recv(1024).decode('utf-8')
                if choice == 'Y':
                    self.request.sendall(str(file_has_size).encode('utf-8'))
                    has_received += file_has_size
                    f = open(abs_path, 'ab')
                else:
                    f = open(abs_path, "wb")
            else:
                # 文件完整存在
                self.request.sendall('801'.encode('utf-8'))
                return
        else:
            self.request.sendall('802'.encode('utf-8'))
            f = open(abs_path, "wb")

        while has_received < file_size:

            data = self.request.recv(1024)
            if not data:  # linux这样！windows需要捕获异常
                break
            f.write(data)
            has_received += len(data)
        f.close()

    def ls(self, **data):
        print(data)
        file_list = os.listdir(self.mainPath)
        file_str = '\n'.join(file_list)
        if not len(file_list):
            file_str = "<Empty dir>"
        self.request.sendall(file_str.encode('utf-8'))

    def cd(self, **data):
        print(data)
        dirname = data.get("dirname")
        if dirname == '..':
            self.mainPath = os.path.dirname(self.mainPath)
        else:
            self.mainPath = os.path.join(self.mainPath, dirname)

        self.request.sendall(self.mainPath.encode('utf-8'))

    def mkdir(self, **data):
        print(data)
        dirname = data.get("dirname")
        path = os.path.join(self.mainPath, dirname)
        if not os.path.exists(path):
            if "/" in dirname:
                os.makedirs(path)
            else:
                os.mkdir(path)
            self.request.sendall("succed!".encode('utf-8'))
        else:
            self.request.sendall("dirname exist".encode('utf-8'))
