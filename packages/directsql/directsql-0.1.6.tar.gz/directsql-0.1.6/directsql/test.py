import sys,os.path
abspath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.abspath(".."))
from sqlgenerator import *
from connector import MysqlPool,MysqlConnector



def func(*args, **kwargs):
    print("*args", *args)
    print("args", args)
    print("**kwargs", **kwargs)
    print("kwargs", kwargs)
    




if __name__ == "__main__":
    # conn = MysqlConnector(string_arg="mysql -uroot -h121.36.85.248 -P9024 -p123456  -Dspider_test")
    # print(conn.database)
    # conn = MysqlPool(string_arg="mysql -uroot -h121.36.85.248 -P9024 -p123456  -Dspider_test")
    # print(conn.database)

    conn_args = {
        'host': '121.36.85.248',
        'port': 9024,
        'password': '123456',
        'database':'spider_test',
    }
    conn = MysqlConnector(host='121.36.85.248', port=9024, password='123456', database='spider_test')
    print(conn.database)
    conn=MysqlPool(host='121.36.85.248', port=9024, password='123456', database='spider_test')
    conn = MysqlConnector(**conn_args)
    print(conn.database)
    conn = MysqlPool(**conn_args)
    print(conn.database)

    