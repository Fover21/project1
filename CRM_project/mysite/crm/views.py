from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
from crm import forms
from crm import models
from django.utils.safestring import mark_safe


# Create your views here.


# 登录
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if auth.authenticate(username=username, password=password):
            return HttpResponse('ok')
    return render(request, 'login.html')


# 注册
def register(request):
    form_obj = forms.Register()
    if request.method == 'POST':
        form_obj = forms.Register(request.POST)
        if form_obj.is_valid():
            # 方式一
            print('form_obj.cleaned_data', form_obj.cleaned_data)
            # form_obj.cleaned_data.pop('re_password')
            # models.UserProfile.objects.create_user(**form_obj.cleaned_data)
            # 方式二
            obj = form_obj.save()
            print('obj', obj)
            obj.set_password('obj.password')
            obj.save()
            return redirect('/login/')
    return render(request, 'register.html', {'form_obj': form_obj})


# 展示客户列表
def customer_list(request):
    customer = models.Customer.objects.all()
    page = pagination.Pagination(request, customer.count())
    return render(request, 'crm/customer_list.html', {
        "customer": customer[page.start:page.end],
        'html_str': page.show_li,
    })


# 测试分页
users = [{'name': 'ward{}'.format(i), 'pwd': 'pwd{}'.format(i)} for i in range(1, 302)]

from utils import pagination


def user_list(request):
    page = pagination.Pagination(request, len(users), per_num=13, max_show=8)

    return render(request, 'user_list.html',
                  {
                      "data": users[page.start:page.end],
                      'html_str': page.show_li
                  })


practice_pagination_data = [{'name': 'ward{}'.format(i), 'pwd': 'pwd{}'.format(i)} for i in range(1, 302)]


# 练习分页

def practice_pagination(request):
    # 当期页面
    try:
        current_page = int(request.GET.get('page', 1))
        print(current_page)
        if current_page <= 0:
            current_page = 1
    except Exception as e:
        current_page = 1
        print(e)
    # 最多显示的页码数
    max_show = 9
    # 在当前的页面左右各显示一般的数据
    half_show = max_show // 2

    # 每页显示的数据条数
    per_num = 10

    # 总数据量
    all_count = len(practice_pagination_data)

    # 页码总数
    total_num, more = divmod(all_count, per_num)
    # 如果有余数
    if more:
        total_num += 1
    # 总页码数小于最大显示数：显示总页数
    if total_num < max_show:
        page_start = 1
        page_end = total_num
    else:
        # 总页码数大于最大显示数：最多显示11个
        if current_page <= half_show:
            page_start = 1
            page_end = max_show
        elif current_page + half_show >= total_num:
            page_end = total_num
            page_start = total_num - max_show + 1
        else:
            page_start = current_page - half_show
            page_end = current_page + half_show

    # 存放<li>标签的列表（目的是为了将所有的事情在服务端都做好，返回html字符串就ok）
    html_list = []

    # 首页操作
    first_li = '<li><a href="/practice_pagination/?page=1">首页</a></li>'
    html_list.append(first_li)

    # 如果已经到了第一页，再点击上一页是不被允许的,
    if current_page == 1:
        prev_li = '<li class="disabled"><a>上一页</a></li>'
    else:
        prev_li = '<li><a href="/practice_pagination/?page={0}">上一页</a></li>'.format(current_page - 1)
    html_list.append(prev_li)

    # 将切片范围内数据展示
    for num in range(page_start, page_end + 1):
        # 如果是当前页面。将此标签选中
        if current_page == num:
            li_html = '<li class="active"><a href="/practice_pagination/?page={0}">{0}</a></li>'.format(num)
        else:
            li_html = '<li><a href="/practice_pagination/?page={0}">{0}</a></li>'.format(num)
        html_list.append(li_html)
    # 当前页面为最后一页，不能再点击下一页
    if current_page == total_num:
        next_li = '<li class="disabled"><a>下一页</a></li>'
    else:
        next_li = '<li><a href="/practice_pagination/?page={}">下一页</a></li>'.format(current_page + 1)
    html_list.append(next_li)

    # 尾页操作
    last_li = '<li><a href="/practice_pagination/?page={}">尾页</a></li>'.format(total_num)
    html_list.append(last_li)

    # 将列表组成字符串
    html_str = mark_safe(''.join(html_list))

    # 切片的起始值
    start = (current_page - 1) * per_num
    print(start)
    # 切片的终止值
    end = current_page * per_num
    print(end)

    return render(request, 'practice_pagination.html', {
        'data': practice_pagination_data[start:end],
        'html_str': html_str,
    })
