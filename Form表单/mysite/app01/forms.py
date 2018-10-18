# __author: busensei
# data: 2018/10/17
from django import forms
from app01 import models
from django.forms import widgets  # 插件
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


def check_name(value):
    if 'xx' in value:
        raise ValidationError("不符合社会主义核心价值观")


# 定义form
class RegForm(forms.Form):
    user = forms.CharField(
        label='用户名',  # 标签的名字
        min_length=6,  # 检验的规则 最小长度
        # initial='默认值',  # 初始值
        disabled=False,  # 禁用
        help_text='请输入用户名',
        error_messages={  # 自定义错误提示
            'min_length': '长度太短！',
            "required": '不能为空'
        }
    )
    pwd = forms.CharField(
        label='密码',
        min_length=6,
        widget=widgets.PasswordInput()
    )
    gender = forms.ChoiceField(
        choices=((1, '男'), (2, '女'), (3, '不详')),
        widget=widgets.RadioSelect()  # 单选
    )

    hobby = forms.ChoiceField(
        # choices=((1, '足球'), (2, '篮球'), (3, '嘿嘿')),
        # choices=models.Hobby.objects.all().values_list('id', 'name'),
        # widget=widgets.RadioSelect()  # 单选
        widget=widgets.SelectMultiple()  # 多选
    )
    phone = forms.CharField(
        label='手机号',
        validators=[
            check_name,
            RegexValidator(r'^1[3-9]\d{9}$', '手机号不符合！'),
        ]
    )

    email = forms.CharField(
        label='邮箱',
        help_text='请输入用户名',
        validators=[
            check_name,
        ]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('1', self.fields['hobby'].choices)
        self.fields['hobby'].choices = models.Hobby.objects.all().values_list('id', 'name')

    # 局部钩子
    # def clean_pwd_again(self):
    #     pwd = self.cleaned_data.get('pwd')
    #     pwd_again = self.cleaned_data.get('pwd_again')
    #     if pwd == pwd_again:
    #         return pwd_again
    #     raise ValidationError('两次密码不一致！')

    # 全局钩子
    # def clean(self):
    #     pwd = self.cleaned_data.get('pwd')
    #     pwd_again = self.cleaned_data.get('pwd_again')
    #     if pwd == pwd_again:
    #         return self.cleaned_data
    #     self.add_error('pwd_again', '两次密码不一致')
    #     raise ValidationError('两次密码不一致！')
