# __author: ward
# data: 2018/10/11

import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_practice.settings")
    import django

    django.setup()

    from app01 import models
