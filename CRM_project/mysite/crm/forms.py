# __author: ward
# data: 2018/10/22
from django import forms
from crm import models


class BaseForm(forms.ModelForm):
    # 给所有的字段加属性
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


# 注册form
class Register(BaseForm):
    re_password = forms.CharField(
        label='确认密码',
        widget=forms.widgets.PasswordInput(attrs={'onblur': "v_repeat()", 'onkeyup': "v_repeat()"}),
        error_messages={
            'required': '密码不能为空',
        },
    )

    class Meta:
        model = models.UserProfile
        # fields = '__all__'  # 所有字段
        fields = ['username', 'name', 'password', 're_password', 'department']  # 选哪些字段
        # exclude = []  # 不包括那些字段
        widgets = {
            'name': forms.widgets.Input(attrs={'onblur': "v_name()", 'onkeyup': "v_name()"}),
            'department': forms.widgets.Select(attrs={'style': "width: 278px"}),
            'username': forms.widgets.EmailInput(attrs={'onblur': "v_name()", 'onkeyup': "v_name()"}),
            'password': forms.widgets.PasswordInput(attrs={'onblur': "v_password()", 'onkeyup': "v_password()"}),
        }

        labels = {
            'username': '用户名',
            'password': '密码',
            'name': '姓名',
            'department': '部门',
        }
        error_messages = {
            'username': {
                'required': '用户名不能为空',
            },
            'password': {
                'required': '密码不能为空',
            },
            'name': {
                'required': '姓名不能为空',
            },

        }

    # 给所有的字段加属性
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    # for field in self.fields:
    #     self.fields[field].widget.attrs.update({"class": "form-control"})

    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')
        if pwd == re_pwd:
            return self.cleaned_data
        self.add_error('re_password', '两次密码不一致')


# 客户form
class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'
        widgets = {
            'course': forms.widgets.SelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


# 更近记录的form
class ConsultRecordForm(BaseForm):
    class Meta:
        model = models.ConsultRecord
        # fields = '__all__'
        exclude = ['delete_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        customer_choice = [(i.id, i) for i in self.instance.consultant.customers.all()]
        customer_choice.insert(0, ('', '--------'))

        # 限制客户是当前销售的私户
        self.fields['customer'].widget.choices = customer_choice
        # 限制跟进人是当前的用户（销售）
        self.fields['consultant'].widget.choices = [(self.instance.consultant.id, self.instance.consultant), ]


# 报名表form
class EnrollmentForm(BaseForm):
    class Meta:
        model = models.Enrollment
        exclude = ['delete_status', 'contract_approved']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 限制当前的客户只能是传的id对应的客户
        self.fields['customer'].widget.choices = [(self.instance.customer_id, self.instance.customer), ]
        # 限制当前可报名的班级是当前客户的意向班级
        self.fields['enrolment_class'].widget.choices = [(i.id, i) for i in self.instance.customer.class_list.all()]


# 班级Form
class ClassForm(BaseForm):
    class Meta:
        model = models.ClassList
        fields = '__all__'


# 课程记录的form
class CourseRecordForm(BaseForm):
    class Meta:
        model = models.CourseRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print(self.instance.re_class_id)
        print(self.instance.re_class)
        print(self.instance.teacher)
        # 限制当前的班级是传过来id的班级
        self.fields['re_class'].widget.choices = [(self.instance.re_class_id, self.instance.re_class), ]
        # 限制当前的班主任是当前用户
        self.fields['teacher'].widget.choices = [(self.instance.teacher_id, self.instance.teacher)]


# 学习记录Form
class StudyRecordForm(BaseForm):
    class Meta:
        model = models.StudyRecord
        fields = ['attendance', 'score', 'homework_note', 'student']
