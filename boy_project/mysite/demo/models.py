from django.db import models

# Create your models here.

__all__ = ["Book", "Publisher", "Author"]


class Book(models.Model):
    title = models.CharField(max_length=32)
    CHOICE = ((1, "python"), (2, "Linux"), (3, 'Go'))
    category = models.IntegerField(choices=CHOICE)
    pub_time = models.DateField()
    publisher = models.ForeignKey(to='Publisher')
    authors = models.ManyToManyField(to="Author")


class Publisher(models.Model):
    title = models.CharField(max_length=32)


class Author(models.Model):
    name = models.CharField(max_length=32)