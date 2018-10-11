from django.contrib import admin
from app01 import models


admin.site.register(models.Person)
admin.site.register(models.Student)
admin.site.register(models.Class)
admin.site.register(models.Teacher)
