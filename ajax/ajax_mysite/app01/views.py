from django.shortcuts import render, HttpResponse, reverse, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt, csrf_protect


@csrf_exempt  # 排除
def login(request):
    return render(request, 'login.html')


def index(request):
    i1, i2, i3 = '', '', ''
    if request.method == 'POST':
        i1 = int(request.POST.get('i1'))
        i2 = int(request.POST.get('i2'))
        i3 = i1 + i2
    return render(request, 'index.html', {
        'i1': i1,
        'i2': i2,
        'i3': i3,
    })


# from django.views.decorators.csrf import ensure_csrf_cookie 全局的第二中配置方法
# @csrf_exempt
def calc(request):
    # csrfmiddlewaretoken = request.POST.get('csrfmiddlewaretoken')
    # print(csrfmiddlewaretoken)
    i1 = int(request.POST.get('i1'))
    i2 = int(request.POST.get('i2'))
    i3 = i1 + i2
    print(request.POST)
    return HttpResponse(i3)


# 上传
def upload(request):
    if request.method == "POST":
        print("FILES", request.FILES)
        file_obj = request.FILES.get("file")
        with open(file_obj.name, "wb") as f:
            for i in file_obj.chunks():
                f.write(i)
        return HttpResponse("success!")


# test
def tt(request):

    if request.method == "POST":
        ret = reverse('uu')
        print(ret)
        return redirect(ret)

    return render(request, 'index.html')