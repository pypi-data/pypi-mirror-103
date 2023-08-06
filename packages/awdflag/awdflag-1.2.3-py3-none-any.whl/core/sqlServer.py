try:
    import pymssql
    from core.exception import AwdExceptions
except Exception as err:
    from core.exception import AwdExceptions
    raise AwdExceptions(str(err))

class MSSQL:
    def __init__(self,host,username,password,db):
        self.host = host
        self.user = username
        self.pwd = password
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise AwdExceptions("请设置数据库信息 !")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise AwdExceptions("连接数据库失败 !")
        else:
            return cur

    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        #查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecNonQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

