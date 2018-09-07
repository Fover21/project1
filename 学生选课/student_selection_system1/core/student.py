#__author: busensei
#data: 2018/8/3
from sys import exit

class Student:
    OPERATE_DIC = [
        ('查看所有课程', 'search_all_course'),
        ('选择课程', 'choice_course'),
        ('查看已选择的课程', 'search_choic_course'),
        ('退出', 'ex')
    ]

    def __init__(self, stu_name):
        self.stu_name = stu_name

    def choice_course(self):  # 选课
        print('选择课程：')
        print('以下为可选课程：')
        with open('../db/course_information.txt', 'r', encoding='utf-8') as f:
            for i in f:
                i = i.split()
                print(i)
        fg = 0
        while 1:
            flg = 0
            course_name = input('请输入选择课程的名字(输入q退出)：')
            if course_name.upper() == 'Q':
                break
            with open('../db/stu_information.txt', 'r', encoding='utf-8') as f:
                f.seek(0)
                for i in f:
                    i = i.split()
                    if i[1] == course_name and i[0] == self.stu_name:
                        print('该课程您已选择！请选其他课程！')
                        flg = 1
                        break
            if flg == 1:
                continue
            if flg == 0:
                with open('../db/course_information.txt', 'r', encoding='utf-8') as f:
                    for i in f:
                        i = i.split()
                        if i[0] == course_name:
                            fg = 1
                            with open('../db/stu_information.txt', 'a', encoding='utf-8') as f:
                                temp = self.stu_name + ' ' + course_name
                                f.write(temp)
                                f.write('\n')
                                f.flush()
                            print('课程已选！')
                            break
                if fg == 1:
                    break
                else:
                    print('课程不存在！')
                    continue

    def search_choic_course(self):  # 查看学生自己所选课程
        print('查看自己所选内容：')
        dic = {}
        flag = 0
        lis = []
        with open('../db/stu_information.txt', 'r', encoding='utf=8') as f:
            for i in f:
                i = i.split()
                # print(i)
                lis.append(i[0])
                if i[0] == self.stu_name:
                    dic.setdefault(self.stu_name, []).append(i[1])
        if self.stu_name in lis:
            flag = 1

        if flag == 1:
            lis = dic[self.stu_name]
            lis = set(lis)
            dic[self.stu_name] = lis
            print(dic)
        else:
            print('您还没有选课程！')

    def search_all_course(self):  # 查看所有课程（所有可选课程)
        print('查看所有课程:')
        with open('../db/course_information.txt', 'r', encoding='utf-8') as f:
            for i in f:
                i = i.split()
                print(i)

    def ex(self):
        exit()


