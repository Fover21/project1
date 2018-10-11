from django.contrib import admin

# Register your models here.

from app02 import models

admin.site.register((models.Author, models.Publisher, models.Book))
