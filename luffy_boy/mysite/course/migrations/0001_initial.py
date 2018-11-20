# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-11-20 11:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户姓名')),
            ],
            options={
                'verbose_name': '11-用户表',
                'verbose_name_plural': '11-用户表',
                'db_table': '11-用户表',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='课程的分类')),
            ],
            options={
                'verbose_name': '01-课程分类表',
                'verbose_name_plural': '01-课程分类表',
                'db_table': '01-课程分类表',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('content', models.TextField(max_length=1024, verbose_name='评论内容')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Account', verbose_name='会员名')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': '10-评价表',
                'verbose_name_plural': '10-评价表',
                'db_table': '10-评价表',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, unique=True, verbose_name='课程的名称')),
                ('course_img', models.ImageField(upload_to='course/%Y-%m', verbose_name='课程的图片')),
                ('course_type', models.SmallIntegerField(choices=[(0, '付费'), (1, 'vip专享'), (2, '学位课程')])),
                ('brief', models.CharField(max_length=1024, verbose_name='课程简介')),
                ('level', models.SmallIntegerField(choices=[(0, '初级'), (1, '中级'), (2, '高级')], default=1)),
                ('status', models.SmallIntegerField(choices=[(0, '上线'), (1, '下线'), (2, '预上线')], default=0)),
                ('pub_date', models.DateField(blank=True, null=True, verbose_name='发布日期')),
                ('order', models.IntegerField(help_text='从上一个课程数字往后排, 建议中间空几个数字', verbose_name='课程顺序')),
                ('study_num', models.IntegerField(help_text='只要有人买课程，订单表加入数据的同时给这个字段+1', verbose_name='学习人数')),
                ('is_free', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Category', verbose_name='课程的分类')),
            ],
            options={
                'verbose_name': '02-课程表',
                'verbose_name_plural': '02-课程表',
                'db_table': '02-课程表',
            },
        ),
        migrations.CreateModel(
            name='CourseChapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter', models.SmallIntegerField(default=1, verbose_name='第几章')),
                ('title', models.CharField(max_length=32, verbose_name='课程章节名称')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_chapters', to='course.Course')),
            ],
            options={
                'verbose_name': '06-课程章节表',
                'verbose_name_plural': '06-课程章节表',
                'db_table': '06-课程章节表',
            },
        ),
        migrations.CreateModel(
            name='CourseDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', models.IntegerField(verbose_name='课时')),
                ('course_slogan', models.CharField(blank=True, max_length=125, null=True, verbose_name='课程口号')),
                ('video_brief_link', models.CharField(blank=True, max_length=255, null=True)),
                ('summary', models.TextField(max_length=2048, verbose_name='课程概述')),
                ('why_study', models.TextField(verbose_name='为什么学习这门课程')),
                ('service', models.TextField(verbose_name='你将获得哪些服务')),
                ('what_to_study_brief', models.TextField(verbose_name='我将学到哪些内容')),
                ('career_improvement', models.TextField(verbose_name='此项目如何有助于我的职业生涯')),
                ('prerequisite', models.TextField(max_length=1024, verbose_name='课程先修要求')),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='course.Course')),
                ('recommend_courses', models.ManyToManyField(blank=True, related_name='recommend_by', to='course.Course')),
            ],
            options={
                'verbose_name': '03-课程详细表',
                'verbose_name_plural': '03-课程详细表',
                'db_table': '03-课程详细表',
            },
        ),
        migrations.CreateModel(
            name='CourseOutline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('order', models.PositiveSmallIntegerField(default=1)),
                ('content', models.TextField(max_length=2048, verbose_name='内容')),
                ('course_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_outline', to='course.CourseDetail')),
            ],
            options={
                'verbose_name': '12-课程大纲表',
                'verbose_name_plural': '12-课程大纲表',
                'db_table': '12-课程大纲表',
            },
        ),
        migrations.CreateModel(
            name='CourseSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='课时')),
                ('section_order', models.SmallIntegerField(help_text='建议每个课时之间空1至2个值，以备后续插入课时', verbose_name='课时排序')),
                ('free_trail', models.BooleanField(default=False, verbose_name='是否可试看')),
                ('section_type', models.SmallIntegerField(choices=[(0, '文档'), (1, '练习'), (2, '视频')], default=2)),
                ('section_link', models.CharField(blank=True, help_text='若是video，填vid,若是文档，填link', max_length=255, null=True)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_sections', to='course.CourseChapter')),
            ],
            options={
                'verbose_name': '07-课程课时表',
                'verbose_name_plural': '07-课程课时表',
                'db_table': '07-课程课时表',
            },
        ),
        migrations.CreateModel(
            name='DegreeCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='学位课程名字')),
            ],
            options={
                'verbose_name': '05-学位课程表',
                'verbose_name_plural': '05-学位课程表',
                'db_table': '05-学位课程表',
            },
        ),
        migrations.CreateModel(
            name='OftenAskedQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField(max_length=1024)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': '09-常见问题表',
                'verbose_name_plural': '09-常见问题表',
                'db_table': '09-常见问题表',
            },
        ),
        migrations.CreateModel(
            name='PricePolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('valid_period', models.SmallIntegerField(choices=[(1, '1天'), (3, '3天'), (7, '1周'), (14, '2周'), (30, '1个月'), (60, '2个月'), (90, '3个月'), (120, '4个月'), (180, '6个月'), (210, '12个月'), (540, '18个月'), (720, '24个月')])),
                ('price', models.FloatField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': '08-价格策略表',
                'verbose_name_plural': '08-价格策略表',
                'db_table': '08-价格策略表',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='讲师名字')),
                ('brief', models.TextField(max_length=1024, verbose_name='讲师介绍')),
            ],
            options={
                'verbose_name': '04-教师表',
                'verbose_name_plural': '04-教师表',
                'db_table': '04-教师表',
            },
        ),
        migrations.AddField(
            model_name='coursedetail',
            name='teachers',
            field=models.ManyToManyField(to='course.Teacher', verbose_name='课程讲师'),
        ),
        migrations.AddField(
            model_name='course',
            name='degree_course',
            field=models.ForeignKey(blank=True, help_text='如果是学位课程，必须关联学位表', null=True, on_delete=django.db.models.deletion.CASCADE, to='course.DegreeCourse'),
        ),
        migrations.AlterUniqueTogether(
            name='pricepolicy',
            unique_together=set([('content_type', 'object_id', 'valid_period')]),
        ),
        migrations.AlterUniqueTogether(
            name='oftenaskedquestion',
            unique_together=set([('content_type', 'object_id', 'question')]),
        ),
        migrations.AlterUniqueTogether(
            name='coursesection',
            unique_together=set([('chapter', 'section_link')]),
        ),
        migrations.AlterUniqueTogether(
            name='courseoutline',
            unique_together=set([('course_detail', 'title')]),
        ),
        migrations.AlterUniqueTogether(
            name='coursechapter',
            unique_together=set([('course', 'chapter')]),
        ),
    ]
