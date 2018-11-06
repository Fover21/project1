from django.shortcuts import render
from app01 import models


# Create your views here.

def user_list(request):
    users = models.User.objects.all()
    return render(request, 'user_list.html', {'users': users})
