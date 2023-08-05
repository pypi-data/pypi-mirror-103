# directsql
​        一个简单的使用python操作mysql的工具，提供了一些类似sql语法的方法，最终拼接成sql。可以很好地处理一些常见场景，不依赖orm 的同时避免手写大量sql。A simple tool using Python to operate MySQL provides some methods similar to SQL syntax, and finally splices into SQL. It can handle some common scenarios very well, and avoid writing a lot of SQL without relying on ORM.

1. 安装

```shell
$ pip3 install directsql
```



 2 . 导入

directsql   目前只提供三个外部类

```
__all__=["SqlGenerator","MysqlSqler","MysqlPool"]
```

导入方式

```python
from directsql.sqlgenerator import SqlGenerator   #该类用于生成sql语句

#下面是一个池化连接对象MysqlPool  和一个简单连接对象 MysqlConnector
from directsql.connector import MysqlPool,MysqlConnector 

```



3. 使用

   3.1 创建连接

   ```python
    # 1. 传入有名参数
      
       conn = MysqlConnector(host='127.0.0.1', port=3306, password='123456', database='test_base')
       print(conn.database)
       conn=MysqlPool(host='127.0.0.1', port=3306, password='123456', database='test_base')
       
      # 也可使用 直接  参数字典
       conn_args = {
           'host': '127.0.0.1',
           'port': 3306,
           'password': '123456',
           'database':'test_base',
       }
       conn = MysqlConnector(**conn_args)
       print(conn.database)
       conn = MysqlPool(**conn_args)
       print(conn.database)
       
    #2 直接使用 字符串   
       #以下字符串是常用的终端 连接命令
       string_arg="mysql -uroot -h127.0.0.1 -P3306 -p123456  -Dtest_base"  
       conn = MysqlConnector(string_arg=string_arg)
       print(conn.database)
       conn = MysqlPool(string_arg=string_arg)
       print(conn.database)
      
       
   ```

   

