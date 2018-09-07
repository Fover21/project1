#__author: busensei
#data: 2018/8/3

def longin():
    print('-----------登录界面---------')
    while 1:
        flag = 0
        username = input('输入账号：')
        password = input('输入密码：')
        with open('../db/regist.txt', 'r', encoding='utf-8') as f:
            for line in f:
                user, pwd, ident = line.split()

                if user == username and pwd == password:
                    print('登录成功！')
                    return username, ident
            else:
                flag = 1
        if flag == 1:
            print('账号密码不存在！请重新输入！')
            continue


if __name__ == '__main__':
    longin()