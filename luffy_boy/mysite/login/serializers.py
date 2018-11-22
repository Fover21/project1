# __author: busensei
# data: 2018/11/22

from rest_framework import serializers
from course.models import Account
import hashlib


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['username', 'pwd']

    def create(self, validated_data):
        username = validated_data['username']
        pwd = validated_data['pwd']
        hash_pwd = hashlib.md5(pwd.encode()).hexdigest()
        user_obj = Account.objects.create(username=username, pwd=hash_pwd)
        return user_obj