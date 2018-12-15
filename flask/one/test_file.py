# # __author: waed
# # data: 2018/12/14
#
# def wrapper1(func):
#     def inner():
#         print('wrapper1 ,before func')
#         func()
#         print('wrapper1 ,after func')
#
#     return inner
#
#
# def wrapper2(func):
#     def inner():
#         print('wrapper2 ,before func')
#         func()
#         print('wrapper2 ,after func')
#
#     return inner
#
#
# @wrapper2
# @wrapper1
# def f():
#     print('in f')
#
#
# f()


def quick_sort(array):
    if len(array) < 2: return array
    return quick_sort([lt for lt in array[1:] if lt < array[0]]) + [array[0]] + quick_sort(
        [ge for ge in array[1:] if ge >= array[0]])


arr = [3, 1, 6, 8, 2, 2, 3]
res = quick_sort(arr)
print(res)

# list
# tuple
# dict
# str
# set