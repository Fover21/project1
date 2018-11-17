from django.contrib import admin
from demo import models
# Register your models here.


for table in models.__all__:
    admin.site.register(getattr(models, table))

# admin.site.register((models.Book, models.Author, models.Publisher))