#__author: busensei
#data: 2018/8/6


path = __file__.split('/')
# print(path)  # ['', 'Users', 'busensei', 'wzy', 'OldBoy', 'Week05', 'Week05作业', 'student_selection_system', 'bin', 'start.py']
path = path[0:-2]
path = '/'.join(path)

course_information = '/'.join([path, 'db', 'course_information.txt'])
regist = '/'.join([path, 'db', 'regist.txt'])
stu_information = '/'.join([path, 'db', 'stu_information.txt'])


if __name__ == '__main__':

    print(course_information)
    print(regist)
    print(stu_information)