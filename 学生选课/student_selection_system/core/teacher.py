#__author: busensei
#data: 2018/8/3

from core.course import Course
from sys import exit
from conf import settings

class Teacher:
    OPERATE_DIC = [
        ('创建课程', 'create_course'),
        ('创造学生', 'create_stu'),
        ('查看所有课程', 'search_all_course'),
        ('查看所有学生', 'search_all_stu'),
        ('查看学生选课情况', 'search_all_stu_choice_course'),
        ('退出', 'ex')
    ]

    def __init__(self, admin_name):
        self.admin_name = admin_name

    def create_course(self):  # 创建课程
        while 1:
            flag = 0
            print('创建课程信息：')
            course_name = input('课程名：')
            with open(settings.course_information, 'r', encoding='utf-8') as f:
                for i in f:
                    i = i.split()
                    if i[0] == course_name:
                        print('课程已存在！重新输入：')
                        flag = 1
                        break
            if flag == 1:
                continue
            course_price = input('课程价格：')
            course_cycle = input('课程周期：')
            course_teacher = input('课程老师：')
            course_obj = Course(course_name, course_price, course_cycle, course_teacher)
            with open(settings.course_information, 'a', encoding='utf-8') as f:
                temp = course_obj.course_name + ' ' + course_obj.course_price + ' ' + course_obj.course_cycle + ' ' + course_obj.course_teacher
                f.write(temp)
                f.write('\n')
                f.flush()
                print('创建成功！')
                break

    def create_stu(self):  # 创建学生账号密码
        while 1:
            flag = 0
            print('创建学生账号：')
            stu_name = input('请输入学生账号：')
            with open(settings.regist, 'r', encoding='utf-8') as f:
                for i in f:
                    i = i.split()
                    if i[0] == stu_name:
                        flag = 1
                        print('以存在！')
                        break
            if flag == 1:
                continue
            stu_pwd = input('请输入学生密码：')
            model = input('请输入权限，Student为学生权限，Teacher为管理员权限：')
            with open(settings.regist, 'a', encoding='utf-8') as f:
                temp = stu_name + ' ' + stu_pwd + ' ' + model
                f.write(temp)
                f.write('\n')
                f.flush()
                print('创建成功！')
                break

    def search_all_course(self):  # 查看所有课程
        print('查看所有课程:')
        with open(settings.course_information, 'r', encoding='utf-8') as f:
            for i in f:
                i = i.split()
                print(i)

    def search_all_stu(self):  # 查看所有学生
        print('查看所有学生：')
        lis = []
        with open(settings.regist, 'r', encoding='utf-8') as f:
            for i in f:
                i = i.split()
                # print(i)
                if i[2] == 'Student':
                    lis.append(i[0])
        print(lis)

    def search_all_stu_choice_course(self):  # 查看学生选择情况
        print('查看学生选课情况：')
        dic = {}
        with open(settings.stu_information, 'r', encoding='utf=8') as f:
            for i in f:
                i = i.split()
                # print(i)
                dic.setdefault(i[0], []).append(i[1])
        print(dic)

    def ex(self):
        exit()