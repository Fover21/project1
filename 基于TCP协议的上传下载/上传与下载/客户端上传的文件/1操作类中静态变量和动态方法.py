#__author: busensei
#data: 2018/7/23


class Person:
    mind = '有思想'
    animal = '高级动物'
    faith = '有信仰'

    def __init__(self, name, sex, age):
        self.name = name
        self.sex = sex
        self.age = age
        print(name, sex, age)


    def work(self):
        print('会工作')

    def shop(self):
        print('可以购物')

# res = Person.__dict__
# print(res)

# res = Person('me', 'man', 32)
# print(res)
# print(res.__dict__)


# print(res)

#操作类中静态变量
# print(res['mind']) #可以查

# res['mind'] = '无脑'#不可以改
# def res['mind']#不可以删
# res['min'] = '很想笑'#不可以增
# print(res['min'])


#操作类中动态方法，一般不这么用
# res['work'](1)
# Person.work(1)