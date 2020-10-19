import requests
import pymysql  #数据库操作模块
from config_sql import *


class MysqlConnection(object):
     """
     mysql操作类，对mysql数据库进行增删改查
     """

     def __init__(self, config):
         # Connect to the database
         self.connection = pymysql.connect(**config)
         self.connection.autocommit(True)
         self.cursor = self.connection.cursor()

     def QueryAll(self, sql):
         """
         查询所有数据
         :param sql:
         :return:
         """
         # 数据库若断开即重连
         self.reConnect()

         self.cursor.execute(sql)
         return self.cursor.fetchall()

     def QueryMany(self, sql, n):
         """
         查询某几条数据数据
         :param sql:
         :return:
         """
         # 数据库若断开即重连
         self.reConnect()

         self.cursor.execute(sql)
         return self.cursor.fetchmany(n)

     def QueryOne(self, sql):
         """
         查询某几条数据数据
         :param sql:
         :return:
         """
         # 数据库若断开即重连
         self.reConnect()

         self.cursor.execute(sql)
         return self.cursor.fetchone()

     # return self.cursor.fetchone()

     def reConnect(self):
         """
         重连机制
         :return:
         """
         try:
             self.connection.ping()
         except:
             self.connection()

     def Operate(self, sql, params=None, DML=True):
         """
         数据库操作:增删改查
         DML: insert / update / delete
         DDL: CREATE TABLE/VIEW/INDEX/SYN/CLUSTER
         """
         try:
             # 数据库若断开即重连
             self.reConnect()

             with self.connection.cursor() as cursor:
                 cursor.execute(sql, params)

                 self.connection.commit()

         except Exception as e:
             if DML:
                 # 涉及DML操作时,若抛异常需要回滚
                 self.connection.rollback()
             print(e)

     def __del__(self):
         """
         MysqlConnection实例对象被释放时调用此方法,用于关闭cursor和connection连接
         """
         self.cursor.close()
         self.connection.close()


if __name__ == "__main__":
    # 初始化MysqlConnection实例对象需要传Mysql配置信息的字典
    config = {'host': MYSQL_HOST, 'charset': CHARSET, 'db': DB, 'user': USER, 'port': MYSQL_PORT, 'password': PASSWORD}
    msc = MysqlConnection(config)
    sql = "delete from users where username ='%s'" % "123456"

    print(msc.Operate(sql))

