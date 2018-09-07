#__author: busensei
#data: 2018/8/3


import sys
from core.login import longin
from core.student import Student
from core.teacher import Teacher

def main():
    usr, id = longin()
    print('user,id:', usr, id)
    print('请输入相应的数字进行相应的操作！')
    file = sys.modules[__name__]
    cls = getattr(file, id)
    obj = cls(usr)
    operate_dic = cls.OPERATE_DIC
    while 1:
        for num, i in enumerate(operate_dic, 1):
            print(num, i[0])

        choice = input('num>>>')
        if choice.isdigit():
            if int(choice) >= 1 and int(choice) <= 6:
                choice_item = operate_dic[int(choice) - 1]
                getattr(obj, choice_item[1])()
            else:
                print('输入有误重新输入！')
                continue
        else:
            print('输入有误重新输入！')
            continue

if __name__ == '__main__':
    main()