=============python操作MySQL============

一、链接，执行sql，关闭（游标）

import pymysql # 导入模块
user= input('用户名：>>').strip()
pwd= input('密码：>>').strip()

#先链接，拿到游标
conn=pymysql.connect(host='localhost',user='root',password='密码', database='数据库名',charset='utf8')
cursor=conn.cursor() #拿到游标，即mysql >
#执行sql
sql='select * from userinfo where user="%s" and password="%s";'%(user,pwd)
print(sql) #注意%s需要加双引号
rows = cursor.execute(sql)  #拿到受影响的行数

cursor.close()
conn.close()

if rows:
    print('登录成功')
else:
    print('登录失败')

二、execute()之sql注入

	- 注意：符号--会注释掉它之后的sql，正确的语法是：--后面至少有一个任意字符

	根本原理：就是根据程序的字符串拼接name='%s',当输入一个xxx'--nnn，我们输入的xxx加'在程序中拼接成一个
	判断条件name='xxx'--nnn'
	\

	-sql注入的两种情况
		1.sql注入之：用户存在，绕过密码
			name' -- 任意字符
		2.sql注入之：用户不存在，绕过用户与密码
			xxx' or 1=1 --任意字符

	解释注入：
		# 原来是我们对sql进行字符串拼接
		# sql="select * from userinfo where name='%s' and password='%s'" %(user,pwd)
		# print(sql)
		# rows=cursor.execute(sql)

		#改写为（execute帮我们做字符串拼接，我们无需且一定不能再为%s加引号了）
		sql="select * from userinfo where name=%s
		 and password=%s" #！！！注意%s需要去掉引号，因为pymysql会自动为我们加上
		rows=cursor.execute(sql,[user,pwd])
		#pymysql模块自动帮我们解决sql注入的问题，只要我们按照pymysql的规矩来。

		-- execute源码解释
		def execute(self, query, args=None):
        """Execute a query

        :param str query: Query to execute.

        :param args: parameters used with query. (optional)
        :type args: tuple, list or dict

        :return: Number of affected rows
        :rtype: int

        If args is a list or tuple, %s can be used as a placeholder in the query.
        If args is a dict, %(name)s can be used as a placeholder in the query.
        """

三、增、删、改、查：conn.commit()

=======增

import pymysql
先链接，拿到游标
conn=pymysql.connect(host='localhost',user='root',password='密码',database='数据库名')
cursor=conn.cursor() #拿到游标，即mysql >
#执行sql   增：
sql='insert into user1(user,password) VALUES (%s,%s)'
print(sql)
# rows = cursor.execute(sql,('xixi',123))  #插入一条记录  #参数：数组。字典。元组
rows = cursor.executemany(sql,[('xixi',123),('aaa',456),('ttt',147)]) #插入多行记录
print('%s row in set (0.00 sec)'%rows)

conn.commit() #提交到数据库
cursor.close()
conn.close()

=======删

import pymysql
#先链接，拿到游标
name=input('>>').strip()
conn=pymysql.connect(host='localhost',user='root',password='密码',database='数据库名')
cursor=conn.cursor() #拿到游标，即mysql >
#执行sql   删：
sql='delete from user1 where user =%s;'  #删除数据
print(sql)
rows = cursor.execute(sql,(name))
print('%s row in set (0.00 sec)'%rows)

conn.commit() #提交到数据库
cursor.close()
conn.close()

=======改

import pymysql
#先链接，拿到游标
id=input('>>').strip()
conn=pymysql.connect(host='localhost',user='root',password='密码',database='数据库名')
cursor=conn.cursor() #拿到游标，即mysql >
#执行sql   改：
sql=' update user1 set password = "5555555" where id=%s;'
print(sql)
rows = cursor.execute(sql,(id))
print('%s row in set (0.00 sec)'%rows)

conn.commit() #提交到数据库
cursor.close()
conn.close()


========查（fetchont,fetchmany.fetchall）

---------查fetchone,fetchmany,fetchall-----------
import pymysql
conn=pymysql.connect(host='localhost',user='root',password='密码',database='数据库名')
cursor=conn.cursor() #拿到游标，即mysql >
#执行sql   查：
sql='select * from user1;'
rows = cursor.execute(sql)

#查单条fetchone
res1=cursor.fetchone()
res2=cursor.fetchone()
res3=cursor.fetchone()
print(res1)
print(res2)
print(res3)
print(res3[0])
#查多条fetchmany
print(cursor.fetchmany(3))
print(cursor.fetchone())
#查所有fetchall
print(cursor.fetchall())
print(cursor.fetchone())

#-------光标的移动--------
#1.绝对路径：从文件的开头位置算起
print(cursor.fetchall())
cursor.scroll(1,mode='absolute')
print(cursor.fetchone())
cursor.scroll(3,mode='absolute')
print(cursor.fetchone())

#2.相对路径：
print(cursor.fetchone())
print(cursor.fetchone())
cursor.scroll(2,mode='relative') #相对于上面的两条向后移两条
print(cursor.fetchone())

print('%s row in set (0.00 sec)' %rows)
cursor.close()
conn.close()

四、获取插入后的最后一条数据的自增ID

------查看表中最后一行的iD
import pymysql
conn=pymysql.connect(host='localhost',user='root',password='喵喵6',database='数据库名',charset='utf8')
cursor=conn.cursor()


sql='insert into user1(user,password) values(%s,%s);'
rows=cursor.execute(sql,('name','123'))
# rows=cursor.executemany(sql,[('aaa','123'),('bbb','123'),('ccc','12323')])
conn.commit()
print(cursor.lastrowid)  #查看表中最后一行的iD

cursor.close()
conn.close()
