from django.shortcuts import render, HttpResponse, redirect, reverse
from django.contrib import auth
from crm import forms
from crm import models
from django.utils.safestring import mark_safe
from django.views import View
from django.db.models import Q
import copy
from django.http import QueryDict
from django.db import transaction
from django.conf import settings


# Create your views here.


# 登录
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        obj = auth.authenticate(username=username, password=password)
        if obj:
            auth.login(request, obj)
            return redirect(reverse('crm:my_customer'))
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
            return redirect(reverse('login'))
    return render(request, 'register.html', {'form_obj': form_obj})


#  注销
def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


# 展示客户列表  公户和私户
def customer_list(request):
    if request.path_info == reverse('crm:my_customer'):
        customer = models.Customer.objects.filter(consultant=request.user)
    else:
        customer = models.Customer.objects.filter(consultant__isnull=True)
    page = pagination.Pagination(request, customer.count(), per_num=8)
    return render(request, 'crm/consultant/customer_list.html', {
        "customer": customer[page.start:page.end],
        'html_str': page.show_li,
    })


# 展示客户列表CBV
class Customer(View):

    def get(self, request):
        # 普通版
        # q = self.get_search_content()
        # 升级版
        q = self.get_search_content(['qq', 'name', 'birthday'])
        if request.path_info == reverse('crm:my_customer'):
            customer = models.Customer.objects.filter(q, consultant=request.user)
        else:
            customer = models.Customer.objects.filter(q, consultant__isnull=True)
        # if request.path_info == reverse('crm:my_customer'):
        #     customer = models.Customer.objects.filter(Q(qq__contains=query) | Q(name__contains=query),
        #                                               consultant=request.user)
        # else:
        #     customer = models.Customer.objects.filter(Q(qq__contains=query) | Q(name__contains=query),
        #                                               consultant__isnull=True)

        # 解决搜索后的url翻页拼接问题
        print('query', request.GET)  # <QueryDict: {'query': [结果]}>
        # query=结果
        print('request.GET.urlencode', request.GET.urlencode())
        # _mutable=True  这样就可以修改了
        # query_params = copy.deepcopy(request.GET)
        query_params = request.GET.copy()  # 为了将查询结果与页数都放到url上
        # query_params._mutable = True

        page = pagination.Pagination(request, customer.count(), query_params, per_num=3)

        # 生成添加按钮
        add_btn, query_params = self.get_add_btn()

        return render(request, 'crm/consultant/customer_list.html', {
            "customer": customer[page.start:page.end],
            'html_str': page.show_li,
            "add_btn": add_btn,
            "query_params": query_params,
        })

    def post(self, request):
        # 处理post提交的action动作
        print(request.POST)
        action = request.POST.get('action')
        if not hasattr(self, action):
            return HttpResponse('not ok')
        ret = getattr(self, action)()
        # 留一个有返回值的接口
        if ret:
            return ret
        # 处理完后
        return self.get(request)

    def multi_apply(self):
        # 公户变私户  # 表锁和行级锁（同时改为私户的话会发生的错误）
        ids = self.request.POST.getlist('id')
        print('ids', ids)
        # 方法一
        # models.Customer.objects.filter(id__in=ids).update(consultant=self.request.user)
        # 方法二
        # self.request.user.customers.add(*models.Customer.objects.filter(id__in=ids))

        # 同一时刻只能一个人来操作
        apply_num = len(ids)
        # 当前销售的客户总量
        all_customer = self.request.user.customers.count()
        # 用户总数不能超过设置值
        if all_customer + apply_num > settings.CUSTOMER_MAX_NUM:
            return HttpResponse('不要太贪心！')
        with transaction.atomic():
            # 事务：
            obj_list = models.Customer.objects.filter(id__in=ids,
                                                      consultant__isnull=True).select_for_update()  # 加锁(行级锁)
            if apply_num == len(obj_list):
                obj_list.update(consultant=self.request.user)
            else:
                return HttpResponse('被别人抢走了！')
        return HttpResponse('ok')

    def multi_pub(self):
        # 私户变公户
        ids = self.request.POST.getlist('id')
        # 方法一
        # models.Customer.objects.filter(id__in=ids).update(consultant=None)
        # 方法二
        self.request.user.customers.remove(*models.Customer.objects.filter(id__in=ids))
        return HttpResponse('ok')

    def multi_delete(self):
        ids = self.request.POST.getlist('id')
        models.Customer.objects.filter(id__in=ids).delete()
        return HttpResponse('ok')

    # 普通版
    # def get_search_content(self):
    #     query = self.request.GET.get('query', '')
    #     q = Q()
    #     q.connector = 'OR'
    #     q.children.append(Q(('qq__contains', query)))
    #     q.children.append(Q(('name__contains', query)))
    #     return q

    # 升级版
    def get_search_content(self, fields_list):
        query = self.request.GET.get('query', '')
        q = Q()
        q.connector = 'OR'
        for i in fields_list:
            q.children.append(Q(('{}__contains'.format(i), query)))
        return q

    # 添加按钮
    def get_add_btn(self):
        # 获取添加按钮
        url = self.request.get_full_path()
        qd = QueryDict()
        qd._mutable = True
        qd['next'] = url
        print(qd)
        query_params = qd.urlencode()
        print('query_params', query_params)
        # add_btn = '<a href="{}?next={}" class="btn btn-primary btn-sm" style="margin-bottom: 10px">添加</a>'.format(
        #     reverse('crm:add_customer'), url)
        # 这是一种给templates加next 的方法，编辑那也是一种直接将next={{ query_params }}
        add_btn1 = '<a href="{}?{}" class="btn btn-primary btn-sm" style="margin-bottom: 10px">添加</a>'.format(
            reverse('crm:add_customer'), query_params)
        # print(add_btn)
        print(add_btn1)
        return mark_safe(add_btn1), query_params


# 增加客户
def add_customer(request):
    # 实例化一个对象
    form_obj = forms.CustomerForm()
    if request.method == 'POST':
        form_obj = forms.CustomerForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('crm:customer'))
    return render(request, 'crm/consultant/add_customer.html', {"form_obj": form_obj})


# 编辑用户
def edit_customer(request, edit_id):
    # 根据id获取用户编辑的对象
    obj = models.Customer.objects.filter(id=edit_id).first()
    form_obj = forms.CustomerForm(instance=obj)
    if request.method == 'POST':
        form_obj = forms.CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('crm:customer'))
    return render(request, 'crm/consultant/edit_customer.html', {"form_obj": form_obj})


# 增加用户和编辑用户写在一起
def add_and_edit_customer(request, edit_id=None):
    obj = models.Customer.objects.filter(id=edit_id).first()
    form_obj = forms.CustomerForm(instance=obj)
    if request.method == 'POST':
        form_obj = forms.CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            # 创建一个新的数据或修改原始数据
            form_obj.save()
            # 获取next
            next = request.GET.get('next')
            print('next', next)
            if next:
                return redirect(next)  # 添加或编辑后url不变
            else:
                return redirect(reverse('crm:customer'))
            # return redirect(reverse('crm:customer'))
    return render(request, 'crm/consultant/add_and_edit.html', {"form_obj": form_obj, "edit_id": edit_id})


# 展示跟进记录
class ConsultRecord(View):
    def get(self, request, customer_id):
        if customer_id == '0':
            all_consult_record = models.ConsultRecord.objects.filter(delete_status__isnull=False,
                                                                     consultant=request.user)
        else:
            all_consult_record = models.ConsultRecord.objects.filter(customer_id=customer_id,
                                                                     delete_status__isnull=False)
            print(all_consult_record)
        return render(request, 'crm/consultant/consult_record_list.html', {'all_consult_record': all_consult_record})

    def post(self, request, customer_id):
        # 处理post提交的action动作
        print(request.POST)
        action = request.POST.get('action')
        if not hasattr(self, action):
            return HttpResponse('not ok')
        ret = getattr(self, action)()
        # 留一个有返回值的接口
        if ret:
            return ret
        # 处理完后
        return self.get(request)

    def multi_delete(self):
        ids = self.request.POST.getlist('id')
        models.ConsultRecord.objects.filter(id__in=ids).delete()
        return HttpResponse('ok')


# 添加跟进记录
def add_consult_record(request):
    form_obj = forms.ConsultRecordForm()
    if request.method == 'POST':
        form_obj = forms.ConsultRecordForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return HttpResponse('ok')
    return render(request, 'crm/consultant/consult_record_add_and_edit.html', {"form_obj": form_obj})


# 编辑跟进记录
def edit_consult_record(request, edit_id):
    obj = models.ConsultRecord.objects.filter(id=edit_id).first()
    form_obj = forms.ConsultRecordForm(instance=obj)
    if request.method == 'POST':
        form_obj = forms.ConsultRecordForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return HttpResponse('ok')
    return render(request, 'crm/consultant/consult_record_add_and_edit.html', {"form_obj": form_obj})


# 添加和编辑跟进记录
def consult_record(request, edit_id=None):
    obj = models.ConsultRecord.objects.filter(id=edit_id).first() or models.ConsultRecord(consultant=request.user)
    form_obj = forms.ConsultRecordForm(instance=obj)
    if request.method == "POST":
        form_obj = forms.ConsultRecordForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('crm:consult_record', args=(0,)))
    return render(request, 'crm/consultant/consult_record_add_and_edit.html', {"form_obj": form_obj})


# 报名表展示
class EnrollmentList(View):

    def get(self, request, customer_id):
        if customer_id == '0':
            all_record = models.Enrollment.objects.filter(delete_status__isnull=False,
                                                          customer__consultant=request.user)
        else:
            all_record = models.Enrollment.objects.filter(customer_id=customer_id,
                                                          delete_status__isnull=False)
            print(all_record)
        query_params = self.get_query_params()
        return render(request, 'crm/consultant/enrollment_list.html', {
            'all_record': all_record,
            'query_params': query_params,
        })

    def post(self, request, customer_id):
        # 处理post提交的action动作
        print(request.POST)
        action = request.POST.get('action')
        if not hasattr(self, action):
            return HttpResponse('not ok')
        ret = getattr(self, action)()
        # 留一个有返回值的接口
        if ret:
            return ret
        # 处理完后
        return self.get(request)

    def multi_delete(self):
        ids = self.request.POST.getlist('id')
        models.Enrollment.objects.filter(id__in=ids).delete()
        return HttpResponse('ok')

    def get_query_params(self):
        url = self.request.get_full_path()
        qd = QueryDict()
        qd._mutable = True
        qd['next'] = url
        query_params = qd.urlencode()
        return query_params


# 添加和编辑报名记录  # 这个是在用户表中体现的
def enrollment(request, customer_id=None, edit_id=None):
    obj = models.Enrollment.objects.filter(id=edit_id).first() or models.Enrollment(customer_id=customer_id)
    form_obj = forms.EnrollmentForm(instance=obj)
    if request.method == 'POST':
        form_obj = forms.EnrollmentForm(request.POST, instance=obj)
        if form_obj.is_valid():
            enrollment_obj = form_obj.save()
            # 修改客户的状态
            enrollment_obj.customer.status = 'signed'
            enrollment_obj.customer.save()
            next = request.GET.get('next')
            if next:
                return redirect(next)
            else:
                return redirect(reverse('crm:my_customer'))
    return render(request, 'crm/consultant/enrollment_add_and_edit.html', {
        "form_obj": form_obj,
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
        if request.method == 'POST':
            current_page = int(request.POST.get('page', 1))
        else:
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
