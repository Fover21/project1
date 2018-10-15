from django.contrib import admin

# Register your models here.

from app02 import models


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    search_fields = ('name', 'city')


admin.site.register(models.Publisher, PublisherAdmin)
admin.site.register((models.Author, models.Book))
