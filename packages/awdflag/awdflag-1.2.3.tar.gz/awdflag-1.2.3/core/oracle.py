# -*- coding:utf-8 -*-
try:
    import cx_Oracle
    import pandas as pd
except Exception as err:
    from core.exception import AwdExceptions

    raise AwdExceptions(str(err))


class ORACLE(object):
    def __init__(self, host, username, password, db='orcl'):
        self.host = host
        self.user = username
        self.pwd = password
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        # self.conn = cx_Oracle.connect(self.user, self.pwd, '{}:1521/self.db'.format(self.host, self.db))
        self.conn = cx_Oracle.connect(self.user + '/' + self.pwd + '@' + self.host + '/' + self.db)
        cursor = self.conn.cursor()
        if not cursor:
            raise (NameError, "连接数据库失败")
        else:
            return cursor

    def ExecQuery(self, sql):
        cursor = self.__GetConnect()
        cursor.execute(sql)
        # 调出数据
        resList = cursor.fetchall()

        # 查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecQueryToDataFrame(self, sql):
        cursor = self.__GetConnect()
        cursor.execute(sql)
        # 调出数据
        resList = cursor.fetchall()
        # cols为字段信息 例如((''))
        cols = cursor.description
        # 查询完毕后必须关闭连接
        self.conn.close()

        # 将数据转换为DataFrame
        col = []
        for i in cols:
            col.append(i[0])
        data = list(map(list, resList))
        data = pd.DataFrame(data, columns=col)

        return data

    def ExecNonQuery(self, sql):
        cursor = self.__GetConnect()
        cursor.execute(sql)
        self.conn.commit()
        self.conn.close()
