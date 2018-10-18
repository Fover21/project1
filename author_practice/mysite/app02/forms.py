# __author: ward
# data: 2018/10/18


from django import forms


class RegForm(forms.Form):

    username = forms.CharField(
        label='用户名',
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput()
    )
    re_password = forms.CharField(
        label='再次确认',
        widget=forms.PasswordInput()
    )

    def clean(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if re_password != password:
            self.add_error('re_password', '两次密码不一致！')


class ChancePwd(forms.Form):
    old_password = forms.CharField(
        label='旧密码',
        widget=forms.PasswordInput()
    )
    new_password = forms.CharField(
        label='新密码',
        widget=forms.PasswordInput()
    )
    re_password = forms.CharField(
        label='再次确认',
        widget=forms.PasswordInput()
    )

    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        re_password = self.cleaned_data.get('re_password')
        if re_password != new_password:
            self.add_error('re_password', '两次密码不一致！')