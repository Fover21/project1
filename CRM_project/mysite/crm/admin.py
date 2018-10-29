from django.contrib import admin
from crm import models

# Register your models here.

admin.site.register([models.Customer, models.ClassList, models.Campuses, models.Enrollment, models.CourseRecord])