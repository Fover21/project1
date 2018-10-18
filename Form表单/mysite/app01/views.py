from django.shortcuts import render, HttpResponse, redirect


# Create your views here.


from app01.forms import RegForm


def register(request):
    name_error = ''
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        if len(user) < 6:
            name_error = 'Name is sort'
        else:
            # 数据合格进行数据库的操作
            return HttpResponse('Register is success')
    return render(request, 'register.html', {'name_error': name_error})


def register2(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():  # 是不是一个合格的数据返回bool值
            # cleaned_data 是经过检验的数据
            print(form_obj.cleaned_data)
            # 去数据库操作
            return HttpResponse('Register is success!')
        # else:
        #     return HttpResponse('Fail')
    return render(request, 'register2.html', {'form_obj': form_obj})