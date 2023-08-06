#coding:utf-8
#!/usr/bin/env python3
try:
    from core.logger import Setlog
    from core.smbUpload import *
    from core.winRmExec import *
    from core.sshUpload import *
    from core.winRmUpload import *
    from core.smbExec import SmbExec
    from core.wmiExec import WmiExec
    from core.checkPort import CheckPort
    from core.psUpload import PsUpload
    from core.sqlServer import MSSQL
    from core.oracle import ORACLE
    from core.zipObj import zipEnc
    import base64
    import json
    import sys
except Exception as err:
    from core.exception import AwdExceptions
    raise AwdExceptions(str(err))

logger = Setlog()

def Usage():
    print('''\nUsage:
    python3 400420WAMPHX.py '[{"ip":"172.16.15.142","name":"flag9","type":"database security"}]'
    ''')

class Awd:
    def __init__(self):
        pass
    def winFile(self,host,username,password,src_path,dst_path,src_code,types="file",noZip=True):
        if noZip:
            with open(src_path, 'w') as f:
                f.write(src_code)

        # 优先使用winrm传输方式
        b00l = WinRmUpload(host, username, password, src_path, dst_path)
        if b00l:
            logger.debug('{0} - {1}: \t文件传输成功 !'.format(host,types))
            return True

        logger.debug('{0} - {1}: \tWinRm 传输文件失败, 采用smb传输 !'.format(host,types))
        # 使用smb传输方式
        conn = SmbConnect(host, username, password)
        b00l = SmbUpload(conn, src_path, dst_path)
        if b00l:
            logger.debug('{0} - {1}: \t文件传输成功 !'.format(host,types))
            return True

        logger.debug('{0} - {1}: \tSMB 传输文件失败, 采用Powershell传输 !'.format(host,types))
        # 使用powershell传输方式
        b00l = PsUpload(host,username,password,dst_path,src_code)
        if b00l:
            logger.debug('{0} - {1}: \t文件传输成功 !'.format(host,types))
            return True
        else:
            logger.debug('{0} - {1}: \t文件传输失败 !'.format(host,types))
            return False

    def linuxFile(self,host,port,username,password,src_path,dst_path,src_code,types="file",noZip=True):
        if noZip:
            with open(src_path, 'w') as f:
                f.write(src_code)

        # 优先使用SFTP传输方式
        if SSHUpload(host,port,username,password,src_path,dst_path,keypath="/root/.ssh/id_rsa"):
            logger.debug('{0} - {1}: \t文件传输成功 !'.format(host, types))
            return True

        logger.debug('{0} - {1}: \tSFTP 传输文件失败, 采用SSH命令传输 !'.format(host, types))

        # 使用SSH命令传输方式
        fileCode = base64.b64encode(src_path.encode('utf-8')).decode()
        command = "echo {0}|base64 -d>{1}".format(fileCode,dst_path)
        if SSHExec(host,port,username,password,command,dst_path,keypath="/root/.ssh/id_rsa"):
            logger.debug('{0} - {1}: \t文件传输成功 !'.format(host, types))
            return True
        logger.debug('{0} - {1}: \t文件传输失败 !'.format(host, types))
        return False

    def linuxMysqldb(self, host, port, username, password, update_cmd, select_cmd, flag, types="DB"):
        SSHExec(host,port,username,password,update_cmd)
        result = SSHExec(host,port,username,password,select_cmd)
        if flag in result:
            logger.debug("{0} - {1}: \t数据库 flag 刷新成功!".format(host,types))
            return True
        else:
            logger.debug("{0} - {1}: \t数据库 flag 刷新失败!".format(host,types))
            return False

    def MysqlDb(self, host, username, password, update_cmd, select_cmd, flag, types="DB"):

        # 刷新数据库flag, 无需检查执行是否成功
        if WinRmExec(host, username, password, update_cmd):
            # 检查数据库flag是否刷新成功
            result = WinRmExec(host, username, password, select_cmd)
        else:
            # 使用 smb 执行命令
            logger.debug('{0} - {1}: \tWinRm 执行命令失败, 采用smb执行 !'.format(host, types))
            if SmbExec(host, username, password, update_cmd):
                result = SmbExec(host, username, password, select_cmd)
            else:
                # 使用 WMI 执行命令
                logger.debug('{0} - {1}: \tSMB 执行命令失败, 采用WMI执行 !'.format(host, types))
                WmiExec(host,username,password,update_cmd)
                result = WmiExec(host, username, password, select_cmd)

        if flag in result:
            logger.debug("{0} - {1}: \t数据库 flag 刷新成功!".format(host,types))
            return True
        else:
            logger.debug("{0} - {1}: \t数据库 flag 刷新失败!".format(host,types))
            return False

    def MssqlDb(self, host, username, password, update_sql, select_sql, flag):
        ms = MSSQL(host=host, username=username, password=password, db="master")
        ms.ExecNonQuery(update_sql.encode('utf-8'))

        reslist = ms.ExecQuery(select_sql)
        for i in reslist:
            if flag in i:
                return True
        return False


    def OracleDb(self, host, username, password, update_sql, select_sql, flag):
        od = ORACLE(host=host, username=username, password=password, db="orcldb")
        od.ExecNonQuery(update_sql.encode('utf-8'))

        reslist = od.ExecQuery(select_sql)
        for i in reslist:
            if flag in i:
                return True
        return False

