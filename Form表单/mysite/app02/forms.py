# __author: ward
# data: 2018/10/17

from django import forms
from django.core.exceptions import ValidationError  # 抛出的校验异常
from django.core.validators import RegexValidator
from django.forms import widgets


def check_name(values):
    if 'sb' in values:
        raise ValidationError('含有非法字符')


class Register(forms.Form):
    email = forms.CharField(
        label='邮箱',
        min_length=8,
        error_messages={
            'min_length': '太短',
            "required": '不能为空',
        },
        validators=[
            RegexValidator(r'@.', '不符合@.')
        ]
    )
    phone = forms.CharField(
        label='手机',
        min_length=11,
        error_messages={
            "required": '不能为空',
        },
        validators=[
            RegexValidator(r'^1[3-9]\d{9}$', '手机号不符合！')
        ]
    )

    name = forms.CharField(
        label='姓名',
        min_length=4,
        error_messages={
            'min_length': '太短',
            "required": '不能为空',
        },
        validators=[
            check_name,
        ]
    )
    gender = forms.ChoiceField(
        choices=((1, '男'), (2, "女")),
        label='性别',
    )
    pwd = forms.CharField(
        label='密码',
        min_length=6,
        error_messages={
            'min_length': '太短',
            "required": '不能为空',
        },
        widget=widgets.PasswordInput(),  # 括号写不写都行
    )
    pwd_again = forms.CharField(
        label='再次确认密码',
        min_length=6,
        error_messages={
            'min_length': '太短',
            "required": '不能为空',
        },
        widget=widgets.PasswordInput(),  # 括号写不写都行
    )

    # 局部钩子
    # def clean_pwd_again(self):
    #     pwd = self.cleaned_data.get('pwd')
    #     pwd_again = self.cleaned_data.get('pwd_again')
    #     if pwd == pwd_again:
    #         return pwd_again
    #     raise ValidationError('两次密码不一致！')

    # 全局钩子
    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        pwd_again = self.cleaned_data.get('pwd_again')
        if pwd == pwd_again:
            return self.cleaned_data
        self.add_error('pwd_again', '两次密码不一致')
        raise ValidationError('两次密码不一致！')