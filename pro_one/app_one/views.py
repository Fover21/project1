from django.shortcuts import render, HttpResponse, redirect
from app_one import models

# Create your views here.


def index(request):
    return render(request, 'index.html')


# 展示出版社信息
def press_list(request):
    # 从数据库中获取数据
    ret = models.Press.objects.all()  # 获取到的是一个列表对象
    return render(request, 'press_list.html', {'result': ret})


# 添加出版社信息
def add_press(request):
    # 如果收到POST发的数据，就将该数据添加到数据库
    if request.method == 'POST':
        # 获取数据
        data = request.POST.get('press_name')
        print(data)
        # 将数据插入数据库
        models.Press.objects.create(name=data)
        # 将插入后的最终结果返回
        return redirect('/press_list/')
    # 否则，不变
    return render(request, 'add_press.html')


# 删除出版社信息
def del_press(request):
    # 现在找到要删除数据的id
    del_id = request.GET.get('id')
    print(del_id)
    # 删除数据库中次id对应的数据
    models.Press.objects.filter(id=del_id).delete()
    # 删除成功后返回删除后的页面
    return redirect('/press_list/')


# 编辑出版社信息
def edit_press(request):
    # 得到编辑这个数据的id
    edit_id = request.GET.get('id')
    # 如果提交更改后的数据
    if request.method == 'POST':
        # 获取更改后的值
        data = request.POST.get('updata_name')
        # 更改数据库中的值
        new_obj = models.Press.objects.filter(id=edit_id)[0]
        new_obj.name = data
        new_obj.save()

        # 将更改后的页面返回
        return redirect('/press_list/')

    # 否则返回数据库中存在的值
    # 获取数据库中的值
    result = models.Press.objects.filter(id=edit_id)[0]
    # 返回当前编辑页面
    return render(request, 'edit_press.html', {'result': result})
