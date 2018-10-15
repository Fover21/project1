# __author: ward
# data: 2018/10/11

import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_practice.settings")
    import django

    django.setup()

    from app02 import models

    # 查找所有书名含有自传的书
    book_obj = models.Book.objects.filter(title__contains="自传").values('title')
    # print(book_obj)

    # 查找出版日期是2018年的书
    book_obj = models.Book.objects.filter(publish_date__year=2018).values('title')
    # print(book_obj)

    # 查找价格大于10元的书名
    book_obj = models.Book.objects.filter(price__gt=100)
    # print(book_obj)

    # 查询价格大于10元的书名和价格
    book_obj = models.Book.objects.filter(price__gt=10).values('title', 'price')
    # print(book_obj)

    # 查找memo字段是空的书
    book_obj = models.Book.objects.filter(memo__isnull=True)
    # print(book_obj)

    # ------------------------------------------

    # 查找在北京出版社出版的书
    press_book_obj = models.Publisher.objects.filter(name='北京出版社').first()
    # 方法一 反向查询
    # titles_obj = press_book_obj.book_set.all()
    # titles = titles_obj.values('title')
    # 方法二 反向查询
    titles = models.Book.objects.filter(publisher__name='北京出版社').values('title')
    # print(titles)

    # 查找名字以北京开头的出版社
    presses = models.Publisher.objects.filter(name__startswith='北京').values('name')
    # print(presses)

    # ----------------------------------------

    # 查找上海出版社出版的所有书籍
    books = models.Book.objects.filter(publisher__name='上海出版社').values('title')
    # print(books)

    # 查找每个出版社出版价格最高的书籍价格
    from django.db.models import Avg, Max, Min, Sum, Count

    # press_books = models.Publisher.objects.annotate(m=Max('books__price'))
    # print(press_books)
    # for i in press_books:
    #     print(i, i.name, i.m)

    # 查找每个出版社的书名以及出的书籍的数量
    # press_books_count = models.Publisher.objects.annotate(book_count=Count('book'))
    # print(press_books_count)
    # for i in press_books_count:
    #     print(i, i.name, i.book_set.all().values('title'),i.book_count)
    ret = models.Publisher.objects.annotate(count=Count('book')).values('name', 'count')
    # print(ret)

    # 查找作者名字里面带有"o"字的作者
    # authors = models.Author.objects.filter(name__contains='o').values('name')
    # print(authors)

    # 查找年龄大于18的作者
    # authors = models.Author.objects.filter(age__gt=18).values('name')
    # print(authors)

    # 查找手机号是155开头的作者
    # authors = models.Author.objects.filter(phone__startswith='155').values('name')
    # print(authors)

    # 查找手机号是155开头的作者的姓名和年龄
    # authors = models.Author.objects.filter(phone__startswith=155).values('name', 'age')
    # print(authors)

    # --------------------------------

    # 查找每个作者写的价格最高的书籍价格
    # author_books_price = models.Author.objects.annotate(m=Max('book__price'))
    # print(author_books_price)
    # for i in author_books_price:
    #     print(i, i.m)

    # 查找每个作者的姓名，以及出的书籍的数量
    # author_books_count = models.Author.objects.annotate(book_counts=Count('book'))
    # print(author_books_count)
    # for i in author_books_count:
    #     print(i, i.book_counts)
    # ret = models.Author.objects.annotate(count=Count('book')).values('name', 'count')
    # print(ret)

    # -----------------------

    # 查找书名是武志洋自传的书的出版社
    # 方法一
    # press = models.Publisher.objects.filter(book__title='武志洋自传').values('name')
    # print(press)
    # 方法二
    # press_obj = models.Book.objects.filter(title='武志洋自传').first()
    # press = press_obj.publisher.name
    # print(press)

    #  查找书名是武志洋自传的书的出版社所在城市
    # press = press_obj.publisher.city
    # print(press)

    # 查找书是武志洋自传的书的出版社名称
    # press_obj = models.Book.objects.filter(title='武志洋自传').first()
    # press = press_obj.publisher.name
    # books = models.Publisher.objects.exclude(name=press).all().values('book__title', 'book__price')
    # print(books)

    # ---------------------------

    # 查找书名是python入门的书的所有作者
    # author = models.Author.objects.filter(book__title='python入门').all().values('name')
    # print(author)

    # 查找书名是python入门的书的所有作者的年龄
    # author = models.Author.objects.filter(book__title='python入门').all().values('name', 'age')
    # print(author)

    # 查找书名是python入门的书的作者的手机号
    # author = models.Author.objects.filter(book__title='python入门').all().values('name', 'age', 'phone')
    # print(author)

    # 查找书名是“python入门”的书的作者们的姓名以及出版的所有书籍名称和价钱
    # author_press_price = models.Author.objects.annotate()
    # print(author_books_price)
    # for i in author_books_price:
    #     print(i, i.name, i.book_set.all().values('title', 'price'))
    ret = models.Author.objects.values('book__title', 'book__price').filter(book__title='python入门').distinct()

    for i in ret:
        print(i)
    from django.db.models import F

    # press_books_count = models.Publisher.objects.annotate(book_count=Count('book'))
    # print(press_books_count)
    # print(press_books_count.all())
    # print(press_books_count.values())
    # for i in press_books_count:
    #     print(i, i.name, i.book_set.all().values('title'),i.book_count)

    # books = models.Book.objects.values("publisher__name").annotate(book_count=Count('title'))
    # print(books)
    # print(books.values())
    # for i in books.values('publisher__name'):
    #     print(i)
