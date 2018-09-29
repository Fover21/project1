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


# 展示书籍信息
def book_list(request):
    # 拿出数据库中书籍的信息
    data = models.Book.objects.all()
    # 展示到页面上
    return render(request, 'book_list.html', {'data': data})


# 添加书籍信息
def add_book(request):
    # 第二次将数据发送来的时候，为POST请求
    if request.method == "POST":
        # 拿到要往数据库添加的数据
        book_name = request.POST.get('book_title')
        title_name = request.POST.get('title_name')
        # 拿到数据后将数据存入数据库
        models.Book.objects.create(title=book_name, press_id=title_name)
        # 存入数据库后将新的页面展现出来
        return redirect('/book_list/')
    # 第一次点击的时候是GET请求，返回添加页面,将选择存在的出版社
    data = models.Press.objects.all()
    return render(request, 'add_book.html', {'data': data})


# 删除书籍信息
def del_book(request):
    # 当点击删除按钮这时，我们应该锁定删除的这一行内容，通过id来获取
    # 那么这个id怎么来了，我们可以将这个id存放到url中，在url中拿到
    del_id = request.GET.get('id')
    # 拿到这个id后将数据库中次id对应的数据删除
    models.Book.objects.filter(id=del_id).delete()
    # 删除数据后重新刷新页面
    return redirect('/book_list/')


# 编辑书籍信息
def edit_book(request):
    # 第一次点击按钮的时候，是get请求，给页面返回这行对应的数据
    # 先拿到这行数据对应的id
    edit_id = request.GET.get('id')
    data = models.Book.objects.filter(id=edit_id)[0]
    # 第二次点击提交数据的时候，将更改后的数据放到数据库
    if request.method == "POST":
        # 获取post传来的书名和出版社名字
        new_book = request.POST.get('title_name')
        new_press = request.POST.get('press_name')
        # 得到这些值后写入数据库
        # 写之前应该先要定位到这一行
        obj = models.Book.objects.filter(id=edit_id)[0]
        obj.title = new_book
        obj.press_id = new_press
        obj.save()
        # 写入数据库后将新的页面呈现
        return redirect('/book_list/')
    data_list = models.Press.objects.all()  # 获取出版社的所有
    return render(request, 'edit_book.html', {'data': data, "data_list": data_list})