from rest_framework import serializers
from demo import models



class PublisherSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=32)


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=32)


# 自定义校验
def my_validate(value):
    if "敏感词汇" in value.lower():
        raise serializers.ValidationError("包含敏感词汇，请重新提交")
    return value


# class BookSerializer(serializers.Serializer):
#     # required=False 反序列化的时候可以没有,只序列化用不走校验
#     id = serializers.IntegerField(required=False)
#     title = serializers.CharField(max_length=32, validators=[my_validate])
#     pub_time = serializers.DateField()
#     # read_only=True 序列化用，反序列化的时候不要了
#     category = serializers.CharField(source="get_category_display", read_only=True)
#     # write_only=True 反序列化 的时候用
#     post_category = serializers.IntegerField(write_only=True)
#
#     publisher = PublisherSerializer(read_only=True)
#     authors = AuthorSerializer(many=True, read_only=True)
#
#     publisher_id = serializers.IntegerField(write_only=True)
#     author_list = serializers.ListField(write_only=True)
#
#     # 重写create方法
#     def create(self, validated_data):
#         # validated_data 校验通过的数据 就是book_obj
#         # 同ORM操作给Book表新增数据
#         book_obj = models.Book.objects.create(
#             title=validated_data['title'],
#             pub_time=validated_data['pub_time'],
#             category=validated_data['post_category'],
#             publisher_id=validated_data['publisher_id']
#         )
#         book_obj.authors.add(*validated_data['author_list'])
#         return book_obj
#
#     def update(self, instance, validated_data):
#         # instance 更新的book_obj对象
#         # validated_data 校验通过的数据
#         # ORM做更新操作
#         instance.title = validated_data.get('title', instance.title)
#         instance.pub_time = validated_data.get('pub_time', instance.pub_time)
#         instance.category = validated_data.get('post_category', instance.category)
#         instance.publisher_id = validated_data.get('publisher_id', instance.publisher_id)
#         if validated_data.get('author_list'):
#             instance.authors.set(validated_data['author_list'])
#         instance.save()
#         return instance
#
#     # 局部钩子校验    单个字段
#     def validate_title(self, value):
#         # value 就是title 的值 对value处理
#         if "python" not in value.lower():
#             raise serializers.ValidationError('标题必须包含python')
#         return value
#
#     # 全局钩子校验    全部字段
#     def validate(self, attrs):
#         # attr 字典有你传过来的所有的字段
#         if "python" in attrs["title"].lower():
#             return attrs
#         else:
#             raise serializers.ValidationError("分类或标题不合符要求")


class BookSerializer(serializers.ModelSerializer):
    # 重写正序
    category_info = serializers.SerializerMethodField(read_only=True)
    publisher_info = serializers.SerializerMethodField(read_only=True)
    authors_info = serializers.SerializerMethodField(read_only=True)

    def get_category_info(self, obj):
        # obj 就是序列化的每一个Book对象
        return obj.get_category_display()

    def get_publisher_info(self, obj):
        # obj 就是序列化的每一个Book对象
        publisher_obj = obj.publisher
        return {"id": publisher_obj.pk, "title": publisher_obj.title}

    def get_authors_info(self, obj):
        # obj 就是序列化的每一个Book对象
        author_qureryset = obj.authors.all()
        return [{"id": author_obj.pk, "name": author_obj.name} for author_obj in author_qureryset]

    class Meta:
        model = models.Book
        fields = "__all__"
        # exclude=["id"]
        # 会让所有的外键关系变成只读read_only=True
        # depth = 1　　 # 向下找几层
        # 反序列化的时候不用自己定义的，而是还是用原来的字段
        extra_kwargs = {"title": {"validators": [my_validate]}, "publisher": {"write_only": True}, "authors": {"write_only": True},
                        "category": {"write_only": True}}

    # 验证
    # 局部钩子校验    单个字段
    def validate_title(self, value):
        # value 就是title 的值 对value处理
        if "python" not in value.lower():
            raise serializers.ValidationError('标题必须包含python')
        return value

    # 全局钩子校验    全部字段
    def validate(self, attrs):
        # attr 字典有你传过来的所有的字段
        if "python1" in attrs["title"].lower():
            return attrs
        else:
            raise serializers.ValidationError("分类或标题不合符要求")
