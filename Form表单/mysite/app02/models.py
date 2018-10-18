from django.db import models

# Create your models here.
# email = forms.CharField()
#     phone = forms.CharField()
#     name = forms.CharField()
#     gender = forms.ChoiceField((1, '男'), (2, "女"))
#     pwd = forms.CharField()
#     pwd_again = forms.CharField()


class RegisterDb(models.Model):
    email = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    gender = models.CharField(max_length=32, choices=((1, '男'), (2, "女")))
    pwd = models.CharField(max_length=32)